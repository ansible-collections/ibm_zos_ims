# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# LICENSE: [GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0)

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}

DOCUMENTATION = r'''
---

module: ims_catalog_populate
short_description: Add datasets to the IMS Catalog
version_added: "2.9"
description:
  - The IMS Catalog Populate utility DFS3PU00 loads, inserts, or updates DBD and PSB instances 
    into the database data sets of the IMS catalog from ACB library data sets.
options:
  irlm_enabled:
    description:
      - Indicates if IRLM is used
    type: bool
    required: false
  irlm_id:
    description:
      - The IRLM id if IRLM is enabled
    type: str
    required: false
  reslib:
    description:
      - Points to an authorized library that contains the IMS SVC modules. 
        The reslib parameter can also be specified in the target inventory's environment_vars.
        The reslib input parameter to the module will take precedence over the value specified in the environment_vars
    type: str
    required: false
  buffer_pool_param_dataset:
    description:
      - Defines the buffer pool parameters data set.
    type: str
    required: true
  primary_log_dataset:
    description:
      - Defines the primary IMS log data set.
    type: dict
    required: true
    suboptions:
      dataset_name:
        description:
          - Describes the name of the dataset
        type: str
        required: true
      disposition:
        description: 
          - Status of dataset
        type: str
        required: false
        choices:
          - NEW
          - OLD
          - SHR
          - EXCL
      record_format:
        description:
          - the record format #Need to expand this
        type: str
        required: false
        choices:
          - FB
          - VB
          - FBA
          - VBA
          - U
      record_length:
        description:
          - the logical record length in bytes #Need to expand this
        type: int
        required: false
      block_size:
        description:
          - the block size #Need to expand this
        type: int
        required: false
      primary:
        description:
          - The amount of primary space to allocate for the dataset
        type: int
        required: false
      primary_unit:
        description:
          - The unit of size to use when specifying primary space
        type: str
        required: false
      secondary:
        description:
          - The amount of secondary space to allocate for the dataset
        type: int
        required: false
      secondary_unit:
        description:
          - The unit of size to sue when specifying secondary space.
        type: str
        required: false
      normal_disposition:
        description:
          - What to do with the dataset after normal termination
        type: str
        required: false
        choices:
          - DELETE
          - KEEP
          - CATLG
          - UNCATLG
      abnormal_disposition:
        description:
          - What to do with the dataset after abnormal termination
        type: str
        required: false
        choices:
          - DELETE
          - KEEP
          - CATLG
          - UNCATLG
      type:
        description: 
          - The type of dataset
        type: str
        required: false
        choices:
          - SEQ
          - BASIC
          - LARGE
          - PDS
          - PDSE
          - LIBRARY
          - LDS
          - RRDS
          - ESDS
          - KSDS
      storage_class:
        description:
          - The storage class for an SMS-managed dataset
        type: str
        required: false
      data_class:
        description:
        type: str
        required: false
      management_class:
        description:
        type: str
        required: false
      key_length:
        description:
        type: int
        required: false
      key_offset:
        description:
        type: int
        required: false
      volumes:
        description:
        type: list
        required: false
        elements: str
      dataset_key_label:
        description: 
        type: str
        required: false
      key_label1:
        description:
        type: str
        required false
      key_encoding1:
        description:
        type: str
        required: false
      key_label2:
        description:
        type: str
        required false
      key_encoding2:
        description:
        type: str
        required: false
  psb_lib:
    description:
      - Defines IMS.PSBLIB dataset
    type: str
    required: true
  dbd_lib:
    description:
      - Defines IMS.DBDLIB datasets
    type: str
    required: true
  proclib:
    description:
      - Defines the IMS.PROCLIB data set that contains the DFSDFxxx member that 
        defines various attributes of the IMS catalog that are required by the utility.
    type: str
    required: true
  steplib:
    description:
      - Points to IMS.SDFSRESL, which contains the IMS nucleus and required IMS modules. 
    type: str
    required: true
  sysin:
    description:
      - A physical sequential dataset that contains the utility control statements that are read by the 
        analysis, purge, and update functions of the DFS3PU10 utility
    type: dict
    required: true
    suboptions:
      mode:
        description:
          - Describes the mode in which the utility executes. 
        type: str
        required: true
        choices:
          - ANALYSIS
          - PURGE
          - BOTH
      deldbver:
        description:
          - Deletes all instances of the specified version of a DBD. When deldbver is specified, ANALYSIS mode or
            BOTH mode must be specified.
        type: list
        required: false
        elements: dict
        suboptions:
          member_name:
            description: 
              - The 8 character name of the DBD that you are deleting a version from.
            type: str
            required: true
          version_number:
            description:
              - The version number of the DBD that you are deleting. The value must match the version number
                that is specified on the DBVER keyword in the DBD generation statement of the version that 
                you are deleting
            type: int
            required: true
      update:
        description:
          - Use this statement to set the retention criteria for records in the catalog database. 
            You can submit any number of update statements. You can submit any number of update statements.
            If a mode statement is supplied with the update statements, the update statements are processed first.
            If mode PURGE is specified, the update statement cannot be specified. 
        type: list
        required: false
        elements: dict
        suboptions:
          resource:
            description:
              - Specifies whether a DBD or PSB should be updated
            choices:
              - DBD
              - PSB
            type: str
            required: true
          member_name:
            description:
              - The 8 character IMS name of the DBD or PSB resource. Wildcards are supported
            type: str
            required: true
          instances:
            description: 
              - The number of instances of a DBD or PSB that must be retained in the DBD or PSB record
            type: int
            required: true
          days: 
            description:
              - The number of days that an instance of a DBD or PSB must be retained before it can be purged
            type: int
            required: false
  sysut1:
    description:
      - A physical sequential data set that contains the DELETE control statements, DELDBVER control 
        statements, or both that are read by the purge function of the utility. 
    type: dict
    required: false
    suboptions:
      deldbver:
        description:
          - Deletes all DBD instances of the specified version of a DBD
        type: list
        required: false
        elements: dict
        suboptions:
          member_name:
            description:
              - The 8 character name of the DBD from which you are deleting a version
            type: str
            required: true
          version_number:
            description:
              - The version number of the DBD that you are deleting. The number that is specified here must match
                the version number that is specified on the DBVER keyword in the DBD generation staement of the version
                that you are deleting
            type: int
            required: true
      delete:
        description:
          - Specifies a DBD or PSB instance or an entire DBD or PSB record to delete from the IMS catalog database.
            When used with PURGE mode, the utility does not check retention criteria, and you can remove DBD or PSB 
            instances that would not otherwise be eligible for deletion.
        type: list:
        required: false
        elements: dict
        suboptions:
          resource:
            description:
              - Specify whether you want to delete a DBD or PSB
            type: str
            required: true
            choices:
              - DBD
              - PSB
          member_name:
            description:
              - The 8 character IMS name of the DBD or PSB resource. Wildcards are supported
            type: str
            required: true 
          time_stamp:
            description:
              - The ACB timestamp that identifies the specific DBD or PSB instance to purge
            type: int
            required: true

author:
  - Jerry Li 
'''

EXAMPLES = r'''

'''

RETURN = r'''




'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.IMSCatalogPopulate.IMSCatalogPopulate import IMSCatalogPopulate # pylint: disable=import-error

def run_module():
    module_args = dict(
      irlm_enabled=dict(type="bool", required=False),
      irlm_id=dict(type="str", required=False),
      reslib=dict(type="str", required=False),
      buffer_pool_param_dataset=dict(type="str", required=False),
      primary_log_dataset=dict(type="dict", required=False),
      psb_lib=dict(type="str", required=False),
      dbd_lib=dict(type="str", required=False),
      proclib=dict(type="str", required=False),
      steplib=dict(type="str", required=False),
      sysin=dict(type="dict", required=True),
      sysut1=dict(type="dict", required=False)
    )

    global module
    module = AnsibleModule(
          argument_spec=module_args,
          supports_check_mode=True
      )
    
    result = {}
    result["changed"] = False

    response = IMSCatalogPopulate(module).execute_catalog_purge()
    
  
    module.exit_json(**response)




def main():
    run_module()

if __name__ == '__main__':
    main()

