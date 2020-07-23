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
  mode:
    description:
      - Indicates what mode the Catalog Populate utility is to be run in.
    type: str
    required: true
    choices:
      - LOAD
      - UPDATE
      - READ
  online_batch:
    description:
      - Indicates if this utility is to be run in a BMP region.
    type: bool
    required: false
    default: false
  ims_id: 
    description:
      - The identifier of the IMS system on which the job is to be run
      - Required if online_batch is true
    type: str
    required: false
  dbrc:
    description:
      - Indicates if IMS Database Recovery Control facility is enabled. 
    type: bool
    required: false
  irlm_id:
    description:
      - The IRLM id if IRLM is enabled. Cannot be specified when online_batch is true. 
    type: str
    required: false
  reslib:
    description:
      - Points to an authorized library that contains the IMS SVC modules. 
    type: list
    required: false
  buffer_pool_param_dataset:
    description:
      - Defines the buffer pool parameters data set.
    type: str
    required: false 
  primary_log_dataset:
    description:
      - Defines the primary IMS log data set. This is required if dbrc is set to true or if
        mode 'UPDATE' is selected
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
          - The record format 
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
          - The logical record length in bytes 
        type: int
        required: false
      block_size:
        description:
          - The block size 
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
      volumes:
        description:
          - A list of volume serials. When providing multiple volumes, processing will begin with
            the first volume in the provided list. Offline volumes are not considered.
        type: list
        required: false
        elements: str
      storage_class:
        description:
          - The storage class for an SMS-managed dataset. Not valid for datasets that are not 
            SMS-managed.
        type: str
        required: false
      management_class:
        description:
          - The management class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
      data_class:
        description:
          - The data class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
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
          - The record format 
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
          - The logical record length in bytes 
        type: int
        required: false
      block_size:
        description:
          - The block size 
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
          - CATALOG
          - UNCATALOG
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
          - CATALOG
          - UNCATALOG
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
      volumes:
        description:
          - A list of volume serials. When providing multiple volumes, processing will begin with
            the first volume in the provided list. Offline volumes are not considered.
        type: list
        required: false
        elements: str
      storage_class:
        description:
          - The storage class for an SMS-managed dataset. Not valid for datasets that are not 
            SMS-managed.
        type: str
        required: false
      management_class:
        description:
          - The management class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
      data_class:
        description:
          - The data class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
  psb_lib:
    description:
      - Defines IMS.PSBLIB dataset
    type: list
    elements: str
    required: true
  dbd_lib:
    description:
      - Defines IMS.DBDLIB datasets
    type: list
    elements: str
    required: true
  check_timestamp:
    description:
      - Determines if the utility should check timestamps of ACB members with duplicate names. 
      - If true, the utility will check if the ACB generation timestamp is different from the previously 
        processed ACB member with the same name. 
      - If the timestamp is different, it will use the ACB with the duplicate name. If not, 
        it will ignore the ACB with the duplicate name. 
    type: bool
    required: false
    default: false
  acb_lib:
    description:
      - Defines an ACB library data set that contains the ACB members that are used to populate the IMS catalog. 
        This DD statement is required.
    type: list
    elements: str
    required: true
  bootstrap_dataset:
    description:
      - Optionally defines the IMS directory bootstrap data set. 
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
      block_size:
        description:
          - The block size 
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
      storage_class:
        description:
          - The storage class for an SMS-managed dataset. Not valid for datasets that are not 
            SMS-managed.
        type: str
        required: false
      management_class:
        description:
          - The management class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
      data_class:
        description:
          - The data class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
  directory_datasets:
    description:
      - Optionally defines the IMS directory data sets that are used to store the ACBs. 
      - If this is omitted, the utility dynamically deletes any preexisting directory datasets 
        and dynamically creates two new datasets to store the ACBs. 
      - The data set name must conform to the same naming convention as for a system-created 
        directory data set.
    type: list
    elements: dict
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
      storage_class:
        description:
          - The storage class for an SMS-managed dataset. Not valid for datasets that are not 
            SMS-managed.
        type: str
        required: false
      management_class:
        description:
          - The management class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
      data_class:
        description:
          - The data class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
  temp_acb_dataset:
    description:
      - An optional control statement to define an empty work data set to be used as an IMS.ACBLIB data set 
        for the IMS Catalog Populate utility. 
      - If IMS Management of ACBs is not enabled, this statement is ommitted. 
      - This dataset does not need to conform to any IMS Catalog or system-defined naming convention
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
      volumes:
        description:
          - A list of volume serials. When providing multiple volumes, processing will begin with
            the first volume in the provided list. Offline volumes are not considered.
        type: list
        required: false
        elements: str
      storage_class:
        description:
          - The storage class for an SMS-managed dataset. Not valid for datasets that are not 
            SMS-managed.
        type: str
        required: false
      management_class:
        description:
          - The management class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
      data_class:
        description:
          - The data class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
  directory_staging_dataset:
    description:
      - Optionally defines the size and placement IMS of the directory staging data set. 
      - The dataset must follow the naming convention for the IMS Catalog Directory.
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
      storage_class:
        description:
          - The storage class for an SMS-managed dataset. Not valid for datasets that are not 
            SMS-managed.
        type: str
        required: false
      management_class:
        description:
          - The management class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
      data_class:
        description:
          - The data class for an SMS-managed dataset. Not valid for datasets taht are not
            SMS-managed
        type: str
        required: false
  proclib:
    description:
      - Defines the IMS.PROCLIB data set that contains the DFSDFxxx member that 
        defines various attributes of the IMS catalog that are required by the utility.
    type: list
    required: true
  steplib:
    description:
      - Points to IMS.SDFSRESL, which contains the IMS nucleus and required IMS modules. 
      - The steplib parameter can also be specified in the target inventory's environment_vars.
      - The steplib input parameter to the module will take precedence over the value specified in the environment_vars.
    type: list
    required: False
  sysabend:
    description:
      - Defines the dump dataset. This defaults to = \* 
    type: str
    required: false
  sysprint:
    description:
      - Defines the output message dataset This defaults to = \* 
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
          - Equivalent to the DUPLIST control statement.
        type: bool
        required: false
        default: false
      print_inserted_resources:
        description:
          - If the IMS management of ACBs is enabled, the utility also lists each DBD or PSB resources that is either added 
            to the IMS directory or saved to the staging data set for importing into the IMS directory later. 
          - Equivalent to the ISRTLIST control statement.
        type: bool
        required: false
        default: true
      max_error_msgs:
        description:
          - Terminate the IMS Catalog Populate utility when more than n messages indicate errors that prevent 
            certain DBDs and PSBs from having their metadata that is written to the IMS catalog.
          - Equivalent to the ERRORMAX=n control statement. 
        type: int
        required: false
      resource_chkp_freq:
        description:
          - Specifies the number of DBD and PSB resource instances to be inserted between checkpoints. 
            n can be a 1 to 8 digit numeric value of 1 to 99999999. 
          - Equivalent to the RESOURCE_CHKP_FREQ=n control statement.
        type: int
        required: false
      segment_chkp_freq:
        description:
          - Specifies the number of segments to be inserted between checkpoints. Can be a 1 to 8 digit numeric value of 1 to 99999999.
          - Equivalent to the SEGMENT_CHKP_FREQ=n control statement.
        type: int
        required: false
      managed_acbs:
        description:
          - Use the MANAGEDACBS control statement to perform the following actions
          - Set up IMS to manage the runtime application control blocks for your databases and program views.
          - Update an IMS system that manages ACBs with new or modified ACBs from an ACB library data set.
          - Save ACBs from an ACB library to a staging data set for later importing into an IMS system that manages ACBs.
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
              clean_staging_dataset:
                description:
                  - If the staging data set is not allocated to any online IMS system, scratch and recreate the staging data 
                    set before adding the resources to the staging data set.
                type: bool
                required: false
                default: false
              gsampcb:
                description:
                  - GSAM resources are included for MANAGEDACBS= running in DLI mode using PSB DFSCP001. 
                  - When GSAMPCB is specified, the IEFRDER batch log data set is not used by the catalog members information gather task.
                  - GSAMPCB and clean_staging_dataset are mutually exclusive.
                type: bool
                required: false
                default: false
              gsamdbd:
                description:
                  - The name of the changed GSAM database. You can use the gsamdbd variable with the STAGE or UPDATE parameter. 
                  - LATEST, UNCOND, DELETE, SHARE, and GSAMPCB are not supported if you specify the gsamdbd variable.          
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
                  - LATEST, UNCOND, DELETE, SHARE, and GSAMPCB are not supported if you specify the gsamdbd variable.          
                type: str
                required: false
                default: false
notes:
  - The I(steplib) parameter can also be specified in the target inventory's environment_vars.
  - The I(steplib) input parameter to the module will take precedence over the value specified in the environment_vars.
  - If only the I(steplib) parameter is specified, then only the I(steplib) concatenation will be used to resolve the IMS RESLIB dataset.
  - Specifying only I(reslib) without I(steplib) is not supported.
author:
  - Jerry Li 
'''

EXAMPLES = r'''
- name: Example of a loading the IMS Catalog
  ims_catalog_populate:
    mode: LOAD
    acb_lib: 
      - SOME.IMS.ACBLIB
    reslib: 
      - SOME.IMS.SDFSRESL
    steplib: 
      - SOME.IMS.SDFSRESL
    proclib: SOME.IMS.PROCLIB
    dbd_lib: SOME.IMS.DBDLIB
    psb_lib: SOME.IMS.PSBLIB
    buffer_pool_param_dataset: "SOME.IMS.PROCLIB(DFSVSMHP)"
    primary_log_dataset:
      dataset_name: SOME.IMS.LOG

- name: Example of loading the IMS Catalog and the IMS Directory datasets with MANAGEDACBS enabled
  ims_catalog_populate:  
    mode: LOAD
    acb_lib: 
      - SOME.IMS.ACBLIB
    reslib: 
      - SOME.IMS.SDFSRESL
    steplib: 
      - SOME.IMS.SDFSRESL
    proclib: SOME.IMS.PROCLIB
    dbd_lib: SOME.IMS.DBDLIB
    psb_lib: SOME.IMS.PSBLIB
    buffer_pool_param_dataset: "SOME.IMS.PROCLIB(DFSVSMHP)"
    control_statements:
      managed_acbs:
        setup: true

- name: Example of updating the IMS Catalog and staging libraries into the IMS directory staging data set
  mode: UPDATE
    acb_lib: 
      - SOME.IMS.ACBLIB
    reslib: 
      - SOME.IMS.SDFSRESL
    steplib: 
      - SOME.IMS.SDFSRESL
    proclib: SOME.IMS.PROCLIB
    dbd_lib: SOME.IMS.DBDLIB
    psb_lib: SOME.IMS.PSBLIB
    buffer_pool_param_dataset: "SOME.IMS.PROCLIB(DFSVSMHP)"
    primary_log_dataset:
      dataset_name: SOME.IMS.LOG
    control_statements:
      managed_acbs:
        stage:
          save_acb: UNCOND
          clean_staging_dataset: true
'''

RETURN = r'''
content:
  description: The standard output returned running the IMS Catalog Populate module
  type: str
  returned: sometimes
  sample: DFS4434I INSTANCE 2020200562326 OF DBD AUTODB   WAS ADDED TO A NEWLY CREATED RECORD IN THE IMS CATALOG.
rc:
  description: The return code from the IMS Catalog Populate utility
  type: str
  returned: sometimes
  sample: '1'
stderr: 
  description: The standard error output returned from running the IMS Catalog Populate
  type: str
  returned: sometimes
msg:
  description: Messages returned from the IMS Catalog Populate module
  type: str
  returned: sometimes
  sample: You cannot define directory datasets, the bootstrap dataset, or directory staging datasets with MANAGEDACBS=STAGE or MANAGEDACBS=UPDATE
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.catalog.catalog import catalog # pylint: disable=import-error
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.catalog_parser.catalog_parser import catalog_parser # pylint: disable=import-error

def run_module():
    module_args = dict(
      mode=dict(type="str", required=True),
      online_batch=dict(type="bool", required=False),
      ims_id=dict(type="str", required=False),
      dbrc=dict(type="bool", required=False),
      irlm_id=dict(type="str", required=False),
      reslib=dict(type="list", required=False),
      buffer_pool_param_dataset=dict(type="str", required=False),
      primary_log_dataset=dict(type="dict", required=False),
      secondary_log_dataset=dict(type="dict", required=False),
      psb_lib=dict(type="list", required=False),
      dbd_lib=dict(type="list", required=False),
      check_timestamp=dict(type="bool", required=False),
      acb_lib=dict(type="list", required=True),
      bootstrap_dataset=dict(type="dict", required=False),
      directory_datasets=dict(type="list", required=False),
      temp_acb_dataset=dict(type="dict", required=False),
      directory_staging_dataset=dict(type="dict", required=False),
      proclib=dict(type="list", required=False),
      steplib=dict(type="list", required=False),
      sysabend=dict(type="str", required=False),
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


