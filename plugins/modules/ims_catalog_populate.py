# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# LICENSE: [GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0)

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}


# ToDo:
# - update dfsreslb to match what is being used for acblib. We also want to be able to take the variable input as precedence but if not supplied will search for an reslib env variable.
# - can add additional detail on buffer pool configuration https://www.ibm.com/support/knowledgecenter/SS6SUT_1.4.0/com.ibm.imstools.bpl14.doc.ug/topics/bplucon_definepools.htm
# - If things are optional, state under what circumstances parameters should or shouldnt be required.
#   Given that the directory datasets are not required regardless of mACB, is this still relevant? Is reslib required?


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
  secondary_log_dataset:
    description:
      - Defines the secondary IMS log data set.
    type: dict
    required: false
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
          - The amount of primary space to allocate for the datatset
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
      normal_dispositon:
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
  check_timestamp:
    description:
      - Determines if the utility should check timestamps of ACB members with duplicate names. 
        If true, the utility will check if the ACB generation timestamp is different from the previously 
        processed ACB member with the same name. If the timestamp is different, it will use the ACB with the
        duplicate name. If not, it will ignore the ACB with the duplicate name. 
    type: bool
    required: false
    default: false
  acb_lib:
    description:
      - Defines additional optional input ACB library data sets. The ddnames of 
        additional ACB libraries will be consecutively numbered. 
    type: list
    elements: str
    required: true
  bootstrap_dataset:
    description:
      - Optionally defines the IMS directory bootstrap data set.
    type: str
    required: false
  directory_datasets:
    description:
      - Optionally defines the IMS directory data sets that are used to store the ACBs. If this is ommitted,
        the utility dynamically deletes any preexisting directory datasets and dynamically creates two new
        datasets to store the ACBs.
    type: list
    elements: str
    required: false
  temp_acb_dataset:
    description:
      - An optional control statement to define an empty work data set to be used 
        as an IMS.ACBLIB data set for the IMS Catalog Populate utility. 
        If IMS Management of ACBs is not enabled, this statement is ommitted. 
    type: str
    required: false
  directory_staging_dataset:
    description:
      - Optionally defines the IMS directory staging data set. 
    type: str
    required: false
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
  sysabend:
    description:
      - Defines the dump dataset
    type: str
    required: false
  sysprint:
    description:
      - Defines the output message dataset
    type: str
    required: false
  control_statements:
    description:
      - The control statement parameters
    type: dict
    required: false
    suboptions:
      print_duplicate_resources:
        description:
          - Specifies that the DFS3PU00 utility list each DBD or PSB resource in the input ACB 
            library that is not added to the IMS catalog because it is a duplicate of an instance 
            that is already in the IMS catalog. 
        type: bool
        required: false
        default: false
      print_inserted_resources:
        description:
          - If the IMS management of ACBs is enabled, the utility also lists each DBD or PSB resources that is either added 
            to the IMS directory or saved to the staging data set for importing into the IMS directory later. 
        type: bool
        required: false
        default: true
      max_error_msgs:
        description:
          - Terminate the IMS Catalog Populate utility when more than n messages indicate errors that prevent 
            certain DBDs and PSBs from having their metadata that is written to the IMS catalog. 
        type: int
        required: false
      resource_chkp_freq:
        description:
          - Specifies the number of DBD and PSB resource instances to be inserted between checkpoints. 
            n can be a 1 to 8 digit numeric value of 1 to 99999999. 
        type: int
        required: false
      segment_chkp_freq:
        description:
          - Specifies the number of segments to be inserted between checkpoints. Can be a 1 to 8 digit numeric value of 1 to 99999999.
        type: int
        required: false
      managed_acbs:
        description:
          - Use the MANAGEDACBS control statement to perform the following actions:
            Set up IMS to manage the runtime application control blocks for your databases and program views.
            Update an IMS system that manages ACBs with new or modified ACBs from an ACB library data set.
            Save ACBs from an ACB library to a staging data set for later importing into an IMS system that manages ACBs.
        type: dict
        required: false
        suboptions:
          setup:
            description:
              - Creates the IMS directory datasets that are required by IMS to manage application control blocks
            type: bool
            required: false
          stage:
            description: 
              - Saves ACBs from the input ACB libraries to a staging dataset.
            type: dict
            required: false
            suboptions:
              save_acb:
                description:
                  - If an ACB already exists in the IMS system, determines if it should be saved unconditionally or by
                    latest timestamp
                required: false
                type: str
                choices:
                  - LATEST
                  - UNCOND
              clean_staging_set:
                description:
                  - If the staging data set is not allocated to any online IMS system, scratch and recreate the staging data 
                    set before adding the resources to the staging data set.
                type: bool
                required: false
                default: false
              gsampcb:
                description:
                  - GSAM resources are included for MANAGEDACBS= running in DLI mode using PSB DFSCP001. When GSAMPCB is specified, 
                    the IEFRDER batch log data set is not used by the catalog members information gather task.
                type: bool
                required: false
                default: false
              gsamdbd:
                description:
                  - The name of the changed GSAM database. You can use the gsamdbd variable with the STAGE or UPDATE parameter. 
                    However, LATEST, UNCOND, DELETE, SHARE, and GSAMPCB are not supported if you specify the gsamdbd variable.          
                type: str
                required: false
                default: false
          update:
            description:
              - Updates existing IMS directory system datasets directly in exclusive mode. The ACBs are not placed in the 
                staging dataset. 
            type: dict
            required: false
            suboptions:
              replace_acb:
                description:
                  - If an ACB already exists in the IMS system, determines if it should be overwritten unconditionally or by
                    latest timestamp
                required: false
                type: str
                choices:
                  - LATEST
                  - UNCOND
              share_mode:
                description:
                  - For dynamic option (DOPT) PSBs only, allocates the required IMS directory data sets in a shared mode 
                    so that DOPT PSBs can be added to the IMS catalog without interrupting online processing.
                type: bool
                required: false
                default: false
              gsampcb:
                description:
                  - GSAM resources are included for MANAGEDACBS= running in DLI mode using PSB DFSCP001. When GSAMPCB is specified, 
                    the IEFRDER batch log data set is not used by the catalog members information gather task.
                type: bool
                required: false
                default: false
              gsamdbd:
                description:
                  - The name of the changed GSAM database. You can use the gsamdbd variable with the STAGE or UPDATE parameter. 
                    However, LATEST, UNCOND, DELETE, SHARE, and GSAMPCB are not supported if you specify the gsamdbd variable.          
                type: str
                required: false
                default: false




author:
  - Jerry Li 
'''

EXAMPLES = r'''

'''

RETURN = r'''




'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.catalog.catalog import catalog # pylint: disable=import-error
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.catalog_parser.catalog_parser import catalog_parser # pylint: disable=import-error

def run_module():
    module_args = dict(
      mode=dict(type="str", required=True),
      irlm_enabled=dict(type="bool", required=False),
      irlm_id=dict(type="str", required=False),
      reslib=dict(type="str", required=False),
      buffer_pool_param_dataset=dict(type="str", required=False),
      primary_log_dataset=dict(type="dict", required=False),
      secondary_log_dataset=dict(type="dict", required=False),
      psb_lib=dict(type="str", required=False),
      dbd_lib=dict(type="str", required=False),
      check_timestamp=dict(type="bool", required=False),
      acb_lib=dict(type="list", required=True),
      bootstrap_dataset=dict(type="str", required=False),
      directory_datasets=dict(type="list", required=False),
      temp_acb_dataset=dict(type="str", required=False),
      directory_staging_dataset=dict(type="str", required=False),
      proclib=dict(type="str", required=False),
      steplib=dict(type="str", required=False),
      control_statements=dict(type="dict", required=False)
    )

    global module
    module = AnsibleModule(
          argument_spec=module_args,
          supports_check_mode=True
      )
    
    result = {}
    result["changed"] = False

    parsed_args=catalog_parser(module, module.params, result).validate_populate_input()
    response = catalog(module, result, parsed_args).execute_catalog_populate()
    
    module.exit_json(**response)




def main():
    run_module()

if __name__ == '__main__':
    main()

