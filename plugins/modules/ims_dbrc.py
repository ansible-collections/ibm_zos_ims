#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r'''
---

module: ims_dbrc

short_description: Submit IMS Database Recovery Control (DBRC) Commands
version_added: "2.9"

description:
  - Use DBRC to record and manage information that is stored in a set of VSAM
    data sets that are collectively called the Recovery Control (RECON) data set.
  - Based on this information, you can use DBRC to advise IMS about how to proceed
    for certain IMS actions.
author:
  - Omar Elbarmawi (@oelbarmawi)
options:
  command:
    description:
      - This is the (well-formatted) DBRC command to submit.
    type: list
    required: true
  dbdlib:
    description:
      - The data set that contains the database descriptions for the databases that are under the control of DBRC.
    type: str
    required: false
  dynalloc:
    description:
      - The DYNALLOC data set that will be used to complete the DBRC execution.
      - Required if `recon` is not specified.
    type: str
    required: false
  genjcl:
    description:
      - The PDS, which contains the JCL and control statements for the utility that DBRC uses to generate a job.
    type: str
    required: false
  recon1:
    description:
      - The RECON1 data set that will be used to complete the DBRC execution.
      - Required if `dynalloc` is not specified.
    type: str
    required: false
  recon2:
    description:
      - The RECON2 data set that will be used to complete the DBRC execution.
    type: str
    required: false
  recon3:
    description:
      - The RECON3 data set that will be used to complete the DBRC execution.
    type: str
    required: false
  steplib:
    description:
      - Points to IMS.SDFSRESL, which contains the IMS nucleus and the required action modules.
    type: str
    required: true
'''

EXAMPLES = '''
- name: Sample DBRC Single Command
  ims_dbrc:
    command: LIST.RECON STATUS
    steplib: IMSBANK.IMS1.SDFSRESL
    dynalloc: IMSTESTL.IMS1.DYNALLOC
    genjcl: IMSTESTL.IMS1.GENJCL
    dbdlib: IMSTESTL.IMS1.DBDLIB

- name: Sample DBRC Multiple Commands
  ims_dbrc:
    command: 
      - LIST.RECON STATUS
      - LIST.DB ALL
      - LIST.DBDS DBD(CUSTOMER)
    steplib: IMSBANK.IMS1.SDFSRESL
    dynalloc: IMSTESTL.IMS1.DYNALLOC
    genjcl: IMSTESTL.IMS1.GENJCL
    dbdlib: IMSTESTL.IMS1.DBDLIB

- name: Sample DBRC Multiple Commands with RECON specified
  ims_dbrc:
    command: 
      - LIST.RECON STATUS
      - LIST.DB ALL
    steplib: IMSBANK.IMS1.SDFSRESL
    genjcl: IMSTESTL.IMS1.GENJCL
    recon1: IMSBANK.IMS1.RECON1
    recon2: IMSBANK.IMS1.RECON2
    recon3: IMSBANK.IMS1.RECON3
    dbdlib: IMSTESTL.IMS1.DBDLIB
'''

RETURN = '''
changed:
  description:
    Indicates if this module effectively modified the target state.
  type: boolean
  returned: always
dbrc_output:
  description:
    The output provided by the specified DBRC Command(s).
  type: list
  returned: sometimes
  contains:
    command:
      description:
        The original command input to the module.
      returned: always
      type: str
    data:
      description:
        Parsed fields from the output content that is mapped to its corresponding value.
      returned: always
      type: dict
    output_content:
      description:
        Unformatted output response from the corresponding DBRC command.
      returned: always
      type: str
failed:
  description:
    Indicates the outcome of the module.
  type: boolean
  returned: always
msg:
  description:
    The output message that the `ims_dbrc` module generates.
  type: str
  returned: always
'''

import json
import re
from os import chmod, path, remove
from tempfile import NamedTemporaryFile
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import ( # pylint: disable=import-error
  DDStatement,
  FileDefinition,
  DatasetDefinition,
  StdoutDefinition,
  StdinDefinition
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_raw import MVSCmd # pylint: disable=import-error
import tempfile
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.import_handler import ( # pylint: disable=import-error
  MissingZOAUImport,
) 

try:
  from zoautil_py import Datasets, types # pylint: disable=import-error
except Exception:
  Datasets = MissingZOAUImport()
  types = MissingZOAUImport()

def verify_dynalloc_recon_requirement(dynalloc, recon1, recon2, recon3):
  # User did not provide dynalloc 
  if not dynalloc:
    # TODO: Determine if each of the RECONs need to be present or just 1 minimum
    if not recon1 or recon2 or recon3:
      return False
  return True
  
def extract_values(elements):
	replacement_values = {
		"** NONE **": None,
		"**NULL**": None,
		"NONE": None,
		"YES": True,
		"NO": False,
		"ON": True,
		"OFF": False
  	}
	fields = {}
	i = 0
	while i < len(elements) - 1:
		key_list = list(filter(None, elements[i].split("  ")))
		value_list = list(filter(None, elements[i + 1].split("  ")))

		last_key_index = len(key_list) - 1
		if len(value_list) == 1 and i > 0 and i < len(elements) - 1: 
			fields[key_list[last_key_index].strip()] = None
		else:
			value = value_list[0].strip()
			if value in replacement_values:
				value = replacement_values[value]
			fields[key_list[last_key_index].strip()] = value
		i += 1

	return fields

def parse_output(raw_output):
	original_output = [elem.strip() for elem in raw_output.split("\n")]
	output_fields = {}
	for line in original_output:
		if "=" in line:
			elements = line.split("=")
			output_fields.update(extract_values(elements))
	return output_fields, original_output
  
# def remove_space(elem):
#   return elem != ' '

def run_module():
  global module
  module_args = dict(
    command=dict(type='list', required=True),
    dbdlib=dict(type='str', required=False),
    dynalloc=dict(type='str', required=False),
    genjcl=dict(type='str', required=False),
    recon1=dict(type='str', required=False),
    recon2=dict(type='str', required=False),
    recon3=dict(type='str', required=False),
    steplib=dict(type='str', required=True)
  )

  result = dict(
    changed=False,
    msg='',
    failed=True,
    dbrc_output=[]
  )
  
  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
  )
  
  """
  Original:
  //DSPURX00 JOB MSGLEVEL=1,MSGCLASS=E,CLASS=K,
  //   LINES=999999,TIME=1440,REGION=0M,       
  //   MEMLIMIT=NOLIMIT                        
  /*JOBPARM  SYSAFF=*                          
  //DSPURX00 EXEC PGM=DSPURX00                 
  //STEPLIB  DD DISP=SHR,                      
  //      DSN=IMSTESTU.IMS1501.MARKER          
  //         DD DISP=SHR,                      
  //      DSN=IMSTESTL.IMS1.EXITLIB            
  //         DD DISP=SHR,                      
  //      DSN=IMSTESTL.IMS1.DYNALLOC           
  //         DD DISP=SHR,                      
  //      DSN=IMSTESTG.IMS15R.TSTRES           
  //         DD DISP=SHR,                      
  //      DSN=IMSBLD.IMS15R.USERLIB            
  //         DD DISP=SHR,                      
  //      DSN=IMSBLD.I15RTSMM.CRESLIB          
  //RECON1   DD DISP=SHR,
  //      DSN=IMSTESTL.IMS1.RECON1
  //RECON2   DD DISP=SHR,
  //      DSN=IMSTESTL.IMS1.RECON2
  //RECON3   DD DISP=SHR,
  //      DSN=IMSTESTL.IMS1.RECON3
  //JCLPDS   DD DISP=SHR,                      
  //      DSN=IMSTESTL.IMS1.GENJCL
  //IMS      DD DISP=SHR,         
  //      DSN=IMSTESTL.IMS1.DBDLIB
  //SYSIN    DD *                 
  ...
  /*                    
  //SYSPRINT DD SYSOUT=*

  Modified:
  //DSPURX00 JOB MSGLEVEL=1,MSGCLASS=E,CLASS=K,
  //   LINES=999999,TIME=1440,REGION=0M,
  //   MEMLIMIT=NOLIMIT
  /*JOBPARM  SYSAFF=*
  //DSPURX00 EXEC PGM=DSPURX00
  //STEPLIB  DD DISP=SHR,
  //      DSN=IMSTESTU.IMS1501.MARKER
  //         DD DISP=SHR,
  //      DSN=IMSBANK2.IMS1.EXITLIB
  //         DD DISP=SHR,
  //      DSN=IMSTESTG.IMS15R.TSTRES
  //         DD DISP=SHR,
  //      DSN=IMSBLD.IMS15R.USERLIB
  //         DD DISP=SHR,
  //      DSN=IMSBLD.I15RTSMM.CRESLIB
  //RECON1   DD DISP=SHR,
  //      DSN=IMSBANK2.IMS1.RECON1
  //RECON2   DD DISP=SHR,
  //      DSN=IMSBANK2.IMS1.RECON2
  //RECON3   DD DISP=SHR,
  //      DSN=IMSBANK2.IMS1.RECON3
  //JCLPDS   DD DISP=SHR,                      
  //      DSN=IMSTESTL.IMS1.GENJCL
  //IMS      DD DISP=SHR,         
  //      DSN=IMSBANK2.IMS1.DBDLIB
  //SYSIN    DD *                 
  //LIST.RECON STATUS
  /*                    
  //SYSPRINT DD SYSOUT=*
  """

  try:
    steplib_datasets = [
      DatasetDefinition("IMSTESTU.IMS1501.MARKER"),
      DatasetDefinition("IMSBANK2.IMS1.EXITLIB"),
      # DatasetDefinition("IMSTESTL.IMS1.DYNALLOC"),
      DatasetDefinition("IMSTESTG.IMS15R.TSTRES"),
      DatasetDefinition("IMSBLD.IMS15R.USERLIB"),
      DatasetDefinition("IMSBLD.I15RTSMM.CRESLIB")
    ]
    steplib = DDStatement("steplib", steplib_datasets)
    recon1 = DDStatement("recon1", DatasetDefinition("IMSBANK2.IMS1.RECON1"))
    recon2 = DDStatement("recon2", DatasetDefinition("IMSBANK2.IMS1.RECON2"))
    recon3 = DDStatement("recon3", DatasetDefinition("IMSBANK2.IMS1.RECON3"))
    jclpds = DDStatement("jclpds", DatasetDefinition("IMSTESTL.IMS1.GENJCL"))
    ims = DDStatement("ims", DatasetDefinition("IMSBANK2.IMS1.DBDLIB"))
    sysin = DDStatement("sysin", [StdinDefinition("  LIST.RECON STATUS"), StdinDefinition("  LIST.DB ALL")])
    sysprint = DDStatement("sysprint", StdoutDefinition())

    response = MVSCmd.execute("dspurx00", [steplib, recon1, recon2, recon3, jclpds, ims, sysin, sysprint])
    fields, original_output = parse_output(response.stdout)
    result["responseobj"] = {
      "rc": response.rc,
      "fields": fields,
      "stdout": original_output,
      "stderr": response.stderr
    }

  except Exception as e:
    result['msg'] = repr(e)
    module.fail_json(**result)
  finally:
      # _delete_data_set(sysin_data_set)
      pass
  module.exit_json(**result)

def main():
  run_module()

if __name__ == '__main__':
  main()