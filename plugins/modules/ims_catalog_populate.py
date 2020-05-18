# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# LICENSE: [GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0)

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}

DOCUMENTATION = r'''
module: ims_catalog_populate
short_description: Add datasets to the IMS Catalog
version_added: "2.9"
description:
  - The IMS Catalog Populate utility DFS3PU00 loads, inserts, or updates DBD and PSB instances 
  - into the database data sets of the IMS catalog from ACB library data sets.
options:
  irlm_enabled:
    description:
      - Indicates if IRLM is used
    type: bool
    required: false
  dfsreslb:
    description:
      - Points to an authorized library that contains the IMS SVC modules.
    type: str
    required: false
  buffer_pool_param_dataset:
    description:
      - Defines the buffer pool parameters data set.
    type: str
    required: false
  primary_log_dataset:
    description:
      - Defines the primary IMS log data set.
    type: str
    required: false
  secondary_log_dataset:
    description:
      - Defines the secondary IMS log data set.
    type: str
    required: false
  psblib:
    description:
      - Defines IMS.PSBLIB datasets
    type: list
    elements: str
    required: false
  dbdlib:
    description:
      - Defines IMS.DBDLIB datasets
    type: list
    elements: str
    required: false
  imsacb01:
    description:
      - Defines an ACBLIB dataset hat contains the ACB members that are used to 
      - populate the IMS catalog. This DD statement is required.
    type: str
    required: true
  additional_acb:
    description:
      - Defines additional optional input ACB library data sets. The ddnames of 
      - additional ACB libraries will be consecutively numbered. 
    type: list
    elements: str
    required: false
  bootstrap_dataset:
    description:
      - Optionally defines the IMS directory bootstrap data set.
    type: str
    required: false
  directory_datasets:
    description:
      - Optionally defines the IMS directory data sets that are used to store the ACBs.
    type: list
    elements: str
    required: false
  temp_acb_dataset:
    description:
      - An optional control statement to define an empty work data set to be used 
      - as an IMS.ACBLIB data set for the IMS Catalog Populate utility.
      - If the IMS management of ACBs is not enabled, this statement is omitted.
      - If this DD statement is omitted, the DFS3PU00 utility dynamically creates a 
      - temporary data set and deletes it after the utility completes processing. 
      - The temp dataset will have defined attributes.
    type: bool
    required: false
  directory_staging_datset:
    description:
      - Optionally defines the IMS directory staging data set. 
      - When you name the data set, conform to the same naming convention as for the staging data set. 
      - The data set must be a PDS-E with DSORG=PO, RECFM=U, LRECL=0, BLKSIZE=32760, DSNTYPE=LIBRARY.
      - The data set must be empty when the utility begins processing the data set.
    type: str
    required: false
  proclib:
    description:
      - Defines the IMS.PROCLIB data set that contains the DFSDFxxx member that 
      - defines various attributes of the IMS catalog that are required by the utility.
    type: str
    required: false
  steplib:
    description:
      - Points to IMS.SDFSRESL, which contains the IMS nucleus and required IMS modules. 
    type: str
    required: false
  sysabend:
    description:
      - Defines the dump data set
    type: str
    required: false
  sysprint:
    description:
      - Defines the output message data set.
    type: str
    required: false
  duplist:
    description:
      - Specifies that the DFS3PU00 utility list each DBD or PSB resource in the input ACB 
      - library that is not added to the IMS catalog because it is a duplicate of an instance 
      - that is already in the IMS catalog. For each duplicate instance of a resource in the IMS catalog, 
      - the utility prints message DFS4436I.
    type: bool
    required: false
  errormax:
    description:
      - Terminate the IMS Catalog Populate utility when more than n messages indicate errors that prevent 
      - certain DBDs and PSBs from having their metadata that is written to the IMS catalog. Duplicate 
      - instances of metadata do not count toward this limit. If this option is omitted, there is no limit.
    type: int
    required: false
  resource_chkp_freq:
    description:
      - Specifies the number of DBD and PSB resource instances to be inserted between checkpoints. 
      - n can be a 1 to 8 digit numeric value of 1 to 99999999. The default value is 100.
    type: int
    required: false
  segment_chkp_freq:
    description:
      - Specifies the number of segments to be inserted between checkpoints. When the number is reached, 
      - IMS finishes inserting all of the segments for the resource instance that is currently being processed 
      - before issuing the checkpoint. n can be a 1 to 8 digit numeric value of 1 to 99999999. The default value is 1000.
    type: int
    required: false
  isrtlist:
    description:
      - If the IMS management of ACBs is enabled, the utility also lists each DBD or PSB resources that is either added 
      - to the IMS directory or saved to the staging data set for importing into the IMS directory later.
    type: bool
    required: false
  managed_acbs:
    description:
      - Use the MANAGEDACBS control statement to perform the following actions
      - Set up IMS to manage the runtime application control blocks for your databases and program views.
      - Update an IMS system that manages ACBs with new or modified ACBs from an ACB library data set.
      - Save ACBs from an ACB library to a staging data set for later importing into an IMS system that manages ACBs.
    type: str
    required: false
author:
  - Jerry Li 
'''

EXAMPLES = r'''

'''

RETURN = r'''




'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
  module_args = dict(
    irlm_enabled=dict(type="bool", required=False),
    dfsreslb=dict(type="str", required=False),
    buffer_pool_param_dataset=dict(type="str", required=False),
    primary_log_dataset=dict(type="str", required=False),
    secondary_log_dataset=dict(type="str", required=False),
    psblib=dict(type="list", required=False),
    dbdlib=dict(type="list", required=False),
    imsacb01=dict(type="str", required=True),
    additional_acb=dict(type="list", required=False),
    bootstrap_dataset=dict(type="str", required=False),
    directory_datasets=dict(type="list", required=False),
    temp_acb_dataset=dict(type="str", required=False),
    directory_staging_dataset=dict(type="str", required=False),
    proclib=dict(type="str", required=False),
    steplib=dict(type="str", required=False),
    sysabend=dict(type="str", required=False),
    sysprint=dict(type="str", required=False),
    duplist=dict(type="bool", required=False),
    errormax=dict(type="int", required=False),
    resource_chkp_freq=dict(type="int", required=False),
    segment_chkp_freq=dict(type="int", required=False),
    isrtlist=dict(type="bool", required=False),
    managed_acbs=dict(type="str", required=False)
  )

  module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

  #This is where zos_raw comes in. Working with Blake on how the calls will actually work.

  #Name of utility catalog populate uses
  program_name = "DFS3PU00"
    
  #This is a program parameter. Default is false:
  #PARM=(DLI,DFS3PU00,DFSCPL00,,,,,,,,,,,Y,N,,,,,,,,,,,,'DFSDF=001')
  #If irlm is enabled the PARM looks like:  PARM=(DLI,DFS3PU00,DFSCP001,,,,,,,,,,,Y,Y,irlmid,,,,,,,,,,,'DFSDF=001')
  is_irlm_enabled = module.params['irlm_enabled']

  #The rest of these are dd statements. Need to figure out how dd statements will be called:
  dfsreslb = module.params['dfsreslb']
  buffer_pool = module.params['buffer_pool_param_dataset']
  primary_log = module.params['primary_log_dataset']
  sec_log = module.params['secondary_log_dataset']
  psblib = module.params['psblib']
  dbdlib = module.params['dbdlib']
  imsacb01 = module.params['imsacb01'] 
  additional_acb = module.params['additional_acb'] #will need to loop through these and append
  bootstrap_dataset = module.params['bootstrap_dataset']
  directory_datasets = module.params['directory_datasets']
  temp_acb_dataset = module.params['temp_acb_dataset']
  directory_staging_dataset = module.params['directory_staging_dataset']
  proclib = module.params['proclib']
  steplib = module.params['steplib']
  sysabend = module.params['sysabend']
  sysprint = module.params['sysprint']

  #duplist to managed_acbs are control statements. They are part of the SYSINP DD statement. I assume these are dd_input
  #Most of them are booleans, in that if you specify "true" in the module input, they appear in the SYSINP DD statement
  #Example: //SYSINP   DD  *              ISRTLIST DUPLIST /*  
  #Above is if user specifies 'duplist: true' and 'isrtlist: true'


  




