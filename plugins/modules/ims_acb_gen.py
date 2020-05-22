#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}
DOCUMENTATION = r'''
---
module: ims_acb_gen
short_description: Generate IMS ACB
version_added: "2.9"
description:
  - The ims_acb_gen module generates an IMS application control block (ACB) necessary for an IMS application program to be scheduled and run. 
  - The ims_dbd_gen and ims_psb_gen modules can be used to generate the associated IMS DBDs and PSBs to be used with the ims_acb_gen module. 
  - The DBD and PSB control blocks will be merged and expanded into an IMS internal format called application control blocks (ACBs).

author:
  - Dipti Gandhi (@ddgandhi)
  - Jerry Li (@th365thli)
options:
  command_input:
    description:
      - This field specifies two command options(BUILD/DELETE).
      - BUILD - Specifies that blocks are built for the named PSBs, which refer to the named DBDs.
      - DELETE - Specifies that blocks are deleted from the ACBLIB data set. The named PSBs and all PSBs that refer to the named DBDs are deleted.
    required: true
    type: str
    choices:
      - BUILD
      - DELETE
  comp:
    description:
      - PRECOMP,POSTCOMP, in any combination, cause the required in-place compression.
      - The default is none.
    type: str
    required: false
    default: none
  psb_name:
    description:
      - The name of the PSB(s). Specifies that blocks are built or deleted for all PSBs that are named on this control statement.
      - This field requires "ALL" or a list of psb names to be specified.
    required: false
    type: list
  dbd_name:
    description:
      - The name of the DBD. Specifies that blocks are built or deleted for this DBD, and for all PSBs that reference this DBD either directly or indirectly through logical relationships.
    required: false
    type: list
  acb_lib:
    description:
      - The ACB Maintenance utility maintains the prebuilt blocks (ACB) library (IMS.ACBLIB). The ACB library is a consolidated library of program (PSB) and database (DBD) descriptions.
      - Through control statements, you can direct the maintenance utility to build all control blocks for all PSBs, for a specific PSB, or for all PSBs that reference a specific DBD.
    required: true
    type: str
  psb_lib:
    description:
      - The ACB Maintenance utility receives input from IMS.PSBLIB data set.
      - The ACB Maintenance utility does not change the PSB in IMS.PSBLIB. If changes are made in PSBs that require changes in the associated PSB,
        make these changes before running the utility.
      - Changes in PSBs might also require modifications to the affected application programs. For example, if a DBD has a segment name changed,
        all PSBs which are sensitive to that segment must have their SENSEG statements changed.
      - Application programs which use this database might also need to be modified.
    required: true
    type: list
  dbd_lib:
    description:
      - The ACB Maintenance utility receives input from IMS.DBDLIB data set.
      - The ACB Maintenance utility does not change the DBD in IMS.DBDLIB. If changes are made in DBDs that require changes in the associated DBD,
        make these changes before running the utility.
    required: true
    type: list
  steplib:
    description:
      - Points to IMS.SDFSRESL, which contains the IMS nucleus and required IMS modules. If STEPLIB is unauthorized by having unauthorized libraries 
        that are concatenated to IMS.SDFSRESL, you must include a DFSRESLB DD statement. 
    required: false
    type: list
  res_lib:
    description:
      - Points to an authorized library that contains the IMS SVC modules. For IMS batch, SDFSRESL and any data set that is concatenated to it on the 
        DFSRESLB DD statement must be authorized through the Authorized Program Facility (APF).
    required: false 
    type: list
  bld_psb:
    description:
      - Specifies whether ACBGEN rebuilds all PSBs that reference a changed DBD in the BUILD DBD=(dbdname) statement.
      - YES indicates that ACBGEN rebuilds all PSBs that reference the changed DBD on the BUILD DBD=(dbdname) statement.
      - NO indicates that ACBGEN does not rebuild PSBs that reference the changed DBD if the changed DBD does not change the physical structure of the database.
    required: false
    type: bool
    default: true
notes:
  - steplib param is optional where user can provide it as a input or else it is taken from environment variables 
  - If user provides only steplib, then only STEPLIB DDs will be provided
  - If user provides both steplib and res_lib(dfsreslb), then both STEPLIB and DFSRESLB DDs will be provided
  - The user is not allowed to supply only res_lib(dfsreslb)
  - SYSUT3/SYSUT4 DD options are not supported.
'''

EXAMPLES = r'''
- name: Example of creating blocks for specific PSB
  ims_acb_gen:
    command_input: BUILD
    COMP: PRECOMP,POSTCOMP
    psb_name:
      - PSB1
      - PSB2
      - PSB3
    dbd_name:
      - DBD1
      - DBD2
    psb_lib:
      - SOME.IMS.PSBLIB1
      - SOME.IMS.PSBLIB2
    dbd_lib:
      - SOME.IMS.DBDLIB1
      - SOME.IMS.DBDLIB2
      - SOME.IMS.DBDLIB3
    acb_lib: SOME.IMS.ACBLIB
    res_lib:
      - SOME.IMS.SDFSRESL1
      - SOME.IMS.SDFSRESL2
    steplib:
      - SOME.IMS.SDFSRESL1
      - SOME.IMS.SDFSRESL2
    bld_psb: no  
- name: Example of creating blocks for all PSBs
  ims_acb_gen:
    command_input: BUILD
    psb_name: ALL
    psb_lib:
      - SOME.IMS.PSBLIB1
    dbd_lib:
      - SOME.IMS.DBDLIB1
    acb_lib: SOME.IMS.ACBLIB
- name: Example of deleting a PSB and DBDs
  ims_acb_gen:
    command_input: DELETE
    psb_name:
      - PSB1
    dbd_name:
      - DBD1
      - DBD2
      - DBD3
      - DBD4
      - DBD5
      - DBD6
    acb_lib: SOME.IMS.ACBLIB
    res_lib:
      - SOME.IMS.SDFSRESL1
'''

RETURN = r'''
msg:
  description: The message of the ACBGEN execution result.
  returned: always
  type: str
  sample: ACBGEN execution is successful.
content:
  description: The response resulting from the execution of the utility.
  returned: on success
  type: list
rc:
  description: The return code for the ansible module.
  returned: always
  type: str
  sample: '0'
changed:
  description:
    - Indicates if any changes were made during module execution.
    - True is always returned unless either a module or JCL failure has occurred.
  returned: always
  type: bool
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.ims_gen_utils import (
    submit_uss_jcl,
)


def run_module():
    module_args = dict(
        command_input=dict(type="str", required=True),
        comp=dict(type="str", required=False, default=""),
        psb_name=dict(type="list", elements="str", required=False),
        dbd_name=dict(type="list", elements="str", required=False),
        acb_lib=dict(type="str", required=True),
        psb_lib=dict(type="list", required=True),
        dbd_lib=dict(type="list", required=True),
        res_lib=dict(type="list", required=False),
        steplib=dict(type="list", required=False),
        bld_psb=dict(type="bool", required=False, default=True),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(rc="0", jobId="")
    jobId = submit_uss_jcl(module)
    result["jobId"] = jobId
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
