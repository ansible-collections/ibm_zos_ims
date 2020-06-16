# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# LICENSE: [GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0)

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}


#1. dont need dash - for description lines when continuation from previous line
#   done
#2. need field for IRLMID
#   done
#3. update dfsreslb to match what is being used for acblib. We also want to be able to take the variable input as precedence but if not supplied will search for an reslib env variable.
#4. can add additional detail on buffer pool configuration https://www.ibm.com/support/knowledgecenter/SS6SUT_1.4.0/com.ibm.imstools.bpl14.doc.ug/topics/bplucon_definepools.htm
#5. If things are optional, state under what circumstances parameters should or shouldnt be required.
#   Given that the directory datasets are not required regardless of mACB, is this still relevant? Is reslib required?
#6. log datasets - Are we going to require them to exist or are we going to support creating those log datasets on the fly?
#   I had assumed these already existed, but if not I am leaning towards requiring them 
#7. update psblib and dbdlib to psb_lib and dbd_lib
#   done
#8. do we need both imsacb01 and additional_acb? Can we have a single acb_lib parameter that takes in a list of datasets, and under the covers we'll handle the DD naming being passed into the RAW interface?
#   We will have a single acb_lib list parameter, and have an additional parameter called check_timestamp
#9. distinguish between what is/isn't required for Managed ACBs. ie. bootstrap dataset, directory datasets
#   done  

#More concise descriptions overall for each of the parameters.

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
  psb_lib:
    description:
      - Defines IMS.PSBLIB datasets
    type: str
    required: false
  dbd_lib:
    description:
      - Defines IMS.DBDLIB datasets
    type: str
    required: false
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
    type: bool
    required: false
  directory_staging_datset:
    description:
      - Optionally defines the IMS directory staging data set. 
    type: str
    required: false
  proclib:
    description:
      - Defines the IMS.PROCLIB data set that contains the DFSDFxxx member that 
        defines various attributes of the IMS catalog that are required by the utility.
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
        library that is not added to the IMS catalog because it is a duplicate of an instance 
        that is already in the IMS catalog. 
        # Lots of if cases in this one regarding managed acb, do I need to list all of them?
    type: bool
    required: false
  errormax:
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
  isrtlist:
    description:
      - If the IMS management of ACBs is enabled, the utility also lists each DBD or PSB resources that is either added 
        to the IMS directory or saved to the staging data set for importing into the IMS directory later.
    type: bool
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
          latest:
            description:
              - If an ACB already exists in the IMS system, do not save an instance of the ACB from an ACB library unless
                the instance in the ACB library has a later timestamp than the ACB in the IMS system.
            type: bool
            required: false
          uncond:
            description:
              - If an ACB already exists in the IMS system, save an instance of the ACB from an ACB library unconditionally, 
                unless the timestamp of the ACB in the ACB library is the same as the timestamp of the ACB in the IMS system. 
            type: bool
            required: false
          delete:
            description:
              - If the staging data set is not allocated to any online IMS system, scratch and recreate the staging data 
                set before adding the resources to the staging data set.
            type: bool
            required: false
          gsampcb:
            description:
              - GSAM resources are included for MANAGEDACBS= running in DLI mode using PSB DFSCP001. When GSAMPCB is specified, 
                the IEFRDER batch log data set is not used by the catalog members information gather task.
            type: bool
            required: false
          gsamdbd:
            description:
              - The name of the changed GSAM database. You can use the gsamdbd variable with the STAGE or UPDATE parameter. 
                However, LATEST, UNCOND, DELETE, SHARE, and GSAMPCB are not supported if you specify the gsamdbd variable.          
            type: str
            required: false
      update:
        description:
          - Updates existing IMS directory system datasets directly in exclusive mode. The ACBs are not placed in the 
            staging dataset. 
        type: dict
        required: false
        suboptions:
          latest:
            description:
              - If an ACB already exists in the IMS system, do not replace it with an instance of the ACB from an ACB library unless
                the instance in the ACB library has a later timestamp than the ACB in the IMS system.
            type: bool
            required: false
          uncond:
            description:
              - If an ACB already exists in the IMS system, replace it with an instance of the ACB from an ACB library unconditionally, 
                unless the timestamp of the ACB in the ACB library is the same as the timestamp of the ACB in the IMS system. 
            type: bool
            required: false
          share:
            description:
              - For dynamic option (DOPT) PSBs only, allocates the required IMS directory data sets in a shared mode 
                so that DOPT PSBs can be added to the IMS catalog without interrupting online processing.
            type: bool
            required: false
          gsampcb:
            description:
              - GSAM resources are included for MANAGEDACBS= running in DLI mode using PSB DFSCP001. When GSAMPCB is specified, 
                the IEFRDER batch log data set is not used by the catalog members information gather task.
            type: bool
            required: false
          gsamdbd:
            description:
              - The name of the changed GSAM database. You can use the gsamdbd variable with the STAGE or UPDATE parameter. 
                However, LATEST, UNCOND, DELETE, SHARE, and GSAMPCB are not supported if you specify the gsamdbd variable.          
            type: str
            required: false
  no_isrtlist:
    description:
      - Do not print a list of inserted resource instances.
    type: bool
    required: false
    
       
     

author:
  - Jerry Li 
'''

EXAMPLES = r'''

'''

RETURN = r'''




'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import ( # pylint: disable=import-error
  DDStatement,
  FileDefinition,
  DatasetDefinition,
  StdoutDefinition,
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser # pylint: disable=import-error
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_raw import MVSCmd # pylint: disable=import-error
import tempfile
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.import_handler import ( # pylint: disable=import-error
  MissingZOAUImport,
) 
import tempfile
import pprint

try:
    from zoautil_py import Datasets, types # pylint: disable=import-error
except Exception:
    Datasets = MissingZOAUImport()
    types = MissingZOAUImport()

module = None


def run_module():
    module_args = dict(
      irlm_enabled=dict(type="bool", required=False),
      irlm_id=dict(type="str", required=False),
      reslib=dict(type="str", required=False),
      buffer_pool_param_dataset=dict(type="str", required=False),
      primary_log_dataset=dict(type="str", required=False),
      secondary_log_dataset=dict(type="str", required=False),
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
      sysabend=dict(type="str", required=False),
      sysprint=dict(type="str", required=False),
      duplist=dict(type="bool", required=False),
      errormax=dict(type="int", required=False),
      resource_chkp_freq=dict(type="int", required=False),
      segment_chkp_freq=dict(type="int", required=False),
      isrtlist=dict(type="bool", required=False),
      managed_acbs=dict(type="dict", required=False),
      no_isrtlist=dict(type="bool", required=False)
    )

    global module
    module = AnsibleModule(
          argument_spec=module_args,
          supports_check_mode=True
      )
    
    result = {}
    result["changed"] = False

    #Validate inputs are correctly formatted datasets
    parsed_args = validate_input(module, result)

    #DD statement Generation
    dDStatementList = []
    imsDatasetList = []
    acbDatasetList = []

    if parsed_args['reslib']:
      dfsreslbDDStatement = DDStatement("DFSRESLB", DatasetDefinition(parsed_args['reslib']))
      dDStatementList.append(dfsreslbDDStatement)
    if parsed_args['buffer_pool_param_dataset']:
      dfsvsampDDStatement = DDStatement("DFSVSAMP", DatasetDefinition(parsed_args['buffer_pool_param_dataset']))
      dDStatementList.append(dfsvsampDDStatement)
    if parsed_args['primary_log_dataset']:
      iefrderDDStatement = DDStatement("IEFRDER", DatasetDefinition(parsed_args['primary_log_dataset']))
      dDStatementList.append(iefrderDDStatement)
    if parsed_args['secondary_log_dataset']:
      iefrder2DDStatement = DDStatement("IEFRDER2", DatasetDefinition(parsed_args['secondary_log_dataset']))
      dDStatementList.append(iefrder2DDStatement)
    
    #Generate DD statements for DBD and PSB libs. If they exist, we attach to an ims dd statement. 
    if parsed_args['psb_lib']:
      psbDataset = DatasetDefinition(parsed_args['psb_lib'])
      imsDatasetList.append(psbDataset)
    if parsed_args['dbd_lib']:
      dbdDatset = DatasetDefinition(parsed_args['dbd_lib'])
      imsDatasetList.append(dbdDatset)
    if imsDatasetList:
      imsDDStatement = DDStatement("ims", imsDatasetList)
      dDStatementList.append(imsDDStatement)

    #Generate DD statements for ACB lib. Behavior is different depending on check_timestamps
    if parsed_args['acb_lib']:
      #Check if check_timestamp is false. If so, then we include all the datasets in a single DD Statement
      if parsed_args['check_timestamp'] is False:
        for i in parsed_args['acb_lib']:
          acbDataset = DatasetDefinition(i)
          acbDatasetList.append(acbDataset)
        acbDDStatement = DDStatement("IMSACBA", acbDatasetList)
        dDStatementList.append(acbDDStatement)
      #If check_timestamp is true, then we generate a dd statement for each dataset
      else:
        acbCount = 1
        for i in parsed_args['acb_lib']:
          if acbCount >= 10:
            acbDDStatement = DDStatement("IMSACB{0}".format(acbCount), DatasetDefinition(i))
            dDStatementList.append(acbDDStatement)
            acbCount += 1
          else:
            acbDDStatement = DDStatement("IMSACB0{0}".format(acbCount), DatasetDefinition(i))
            dDStatementList.append(acbDDStatement)
            acbCount += 1
        acbCount = 1
      
    if parsed_args['bootstrap_dataset']:
      btstrDataset = DDStatement("IMSDBSDS", DatasetDefinition(parsed_args['bootstrap_dataset']))
      dDStatementList.append(btstrDataset)
    
    if parsed_args['directory_datasets']:
      directoryCount = 1
      for i in parsed_args['directory_datasets']:
        if acbCount >= 10:
          directoryDDStatement = DDStatement("IMSD00{0}".format(directoryCount), DatasetDefinition(i))
          dDStatementList.append(directoryDDStatement)
        else:
          directoryDDStatement = DDStatement("IMSD000{0}".format(directoryCount), DatasetDefinition(i))
          dDStatementList.append(directoryDDStatement)
    
    if parsed_args['temp_acb_dataset']:
      tempDDStatement = DDStatement("IMSDG001", DatasetDefinition(parsed_args['temp_acb_dataset']))
      dDStatementList.append(tempDDStatement)
    
    if parsed_args['directory_staging_dataset']:
      dirDDStatement = DDStatement("IMDSTAG", DatasetDefinition(parsed_args['directory_staging_dataset']))
      dDStatementList.append(dirDDStatement)
    
    if parsed_args['sysabend']:
      abendDDStatement = DDStatement('SYSABEND', DatasetDefinition(parsed_args['sysabend']))
      dDStatementList.append(abendDDStatement)

    if parsed_args['proclib']:
      proclibDDStatement = DDStatement("PROCLIB", DatasetDefinition(parsed_args['proclib']))
      dDStatementList.append(proclibDDStatement)

    if parsed_args['steplib']:
      steplibDDStatement = DDStatement("STEPLIB", DatasetDefinition(parsed_args['steplib']))
      dDStatementList.append(steplibDDStatement)

    #Add sysprint dd statement
    sysprint = DDStatement("sysprint", StdoutDefinition())
    dDStatementList.append(sysprint)

    irlm_id = ""
    irlm_flag = "N"
    if parsed_args['irlm_enabled']:
      if parsed_args['irlm_id']:
        irlm_id = parsed_args['irlm_id']
        irlm_flag = "Y"
      else: 
        result['msg'] = "You must specify an irlm id"
        module.fail_json(**result)

    paramString = "DLI,DFS3PU00,DFSCPL00,,,,,,,,,,,N,{0},{1},,,,,,,,,,,'DFSDF=CAT'".format(irlm_flag, irlm_id)

    try:
        response = MVSCmd.execute("DFS3PU00", dDStatementList, paramString)
        result["responseobj"] = {
            "rc": response.rc,
            "stdout": response.stdout,
            "stderr": response.stderr,
        }
    except Exception as e:
        module.fail_json(msg=repr(e), **result)
    finally:
        module.exit_json(**result)
    
    



    # try:
    #     temp_data_set_name = _create_temp_data_set("OMVSADM")
    #     _write_data_set(
    #         temp_data_set_name, " DELETE {0}".format(psb_lib[0].upper())
    #     )
    #     sysin = DDStatement("sysin", DatasetDefinition(temp_data_set_name))
    #     sysprint = DDStatement("sysprint", StdoutDefinition())
    #     response = MVSCmd.execute_authorized("idcams", [sysin, sysprint])
    #     result["responseobj"] = {
    #         "rc": response.rc,
    #         "stdout": response.stdout,
    #         "stderr": response.stderr,
    #     }
    # except Exception as e:
    #     module.fail_json(msg=repr(e), **result)
    # finally:
    #     _delete_data_set(temp_data_set_name)

    module.exit_json(**result)

def _create_temp_data_set(hlq):
    """Create a temporary data set.

    Arguments:
        hlq {str} -- The HLQ to use for the temporary data set's name.

    Returns:
        str -- The name of the temporary data set.
    """
    temp_data_set_name = Datasets.temp_name(hlq)
    _create_data_set(
        temp_data_set_name, {"type": "SEQ", "size": "5M", "format": "FB", "length": 80},
    )
    return temp_data_set_name

def _create_data_set(name, extra_args=None):
    """A wrapper around zoautil_py
    Dataset.create() to raise exceptions on failure.

    Arguments:
        name {str} -- The name of the data set to create.

    Raises:
        DatasetCreateError: When data set creation fails.
    """
    if extra_args is None:
        extra_args = {}
    rc = Datasets.create(name, **extra_args)
    if rc > 0:
        raise DatasetCreateError(name, rc)
    return

def _write_data_set(name, contents):
    """Write text to a data set.

    Arguments:
        name {str} -- The name of the data set.
        contents {str} -- The text to write to the data set.

    Raises:
        DatasetWriteError: When write to the data set fails.
    """
    # rc = Datasets.write(name, contents)
    temp = tempfile.NamedTemporaryFile(delete=False)
    with open(temp.name, "w") as f:
        f.write(contents)
    rc, stdout, stderr = module.run_command(
        "cp -O u {0} \"//'{1}'\"".format(temp.name, name)
    )
    if rc != 0:
        raise DatasetWriteError(name, rc, stderr)
    return

def _delete_data_set(name):
    """A wrapper around zoautil_py
    Dataset.delete() to raise exceptions on failure.

    Arguments:
        name {str} -- The name of the data set to delete.

    Raises:
        DatasetDeleteError: When data set deletion fails.
    """
    rc = Datasets.delete(name)
    if rc > 0:
        raise DatasetDeleteError(name, rc)
    return

def validate_input(module, result):
    try:
      module_defs = dict(
        irlm_enabled=dict(arg_type="bool", required=False),
        irlm_id=dict(arg_type="str", required=False),
        reslib=dict(arg_type="data_set", required=False),
        buffer_pool_param_dataset=dict(arg_type="data_set", required=False),
        primary_log_dataset=dict(arg_type="data_set", required=False),
        secondary_log_dataset=dict(arg_type="data_set", required=False),
        psb_lib=dict(arg_type="data_set", required=False),
        dbd_lib=dict(arg_type="data_set", required=False),
        check_timestamp=dict(arg_type="bool", required=False),
        acb_lib=dict(arg_type="list", elements="data_set", required=True),
        bootstrap_dataset=dict(arg_type="data_set", required=False),
        directory_datasets=dict(arg_type="list", elements="data_set", required=False),
        temp_acb_dataset=dict(arg_type="data_set", required=False),
        directory_staging_dataset=dict(arg_type="data_set", required=False),
        proclib=dict(arg_type="data_set", required=False),
        steplib=dict(arg_type="data_set", required=False),
        sysabend=dict(arg_type="str", required=False),
        sysprint=dict(arg_type="str", required=False),
        duplist=dict(arg_type="bool", required=False),
        errormax=dict(arg_type="int", required=False),
        resource_chkp_freq=dict(arg_type="int", required=False),
        segment_chkp_freq=dict(arg_type="int", required=False),
        isrtlist=dict(arg_type="bool", required=False),
        managed_acbs=dict(arg_type="dict", required=False),
        no_isrtlist=dict(arg_type="bool", required=False),
      )

      parser = BetterArgParser(module_defs)
      parsed_args = parser.parse_args(module.params)

      if parsed_args['directory_staging_dataset'] is not None:
        validate_directory_staging_dataset(parsed_args['directory_datasets'], result, module)


      return parsed_args
    except ValueError as error:
      result['msg'] = error.args
      result['rc']=1
      module.fail_json(**result)

def validate_directory_staging_dataset(dset, result, module):
    if len(dset) > 20:
      result['msg'] = "You cannot specify more than 20 IMS directory datasets"
      module.fail_json(**result)

class Error(Exception):
    def __init__(self, *args):
        super(Error, self).__init__(*args)

class DatasetWriteError(Error):
    def __init__(self, data_set, rc, message=""):
        self.msg = 'An error occurred during write of data set "{0}". RC={1}. {2}'.format(
            data_set, rc, message
        )
        super(DatasetWriteError, self).__init__(self.msg)

class DatasetDeleteError(Error):
    def __init__(self, data_set, rc):
        self.msg = 'An error occurred during deletion of data set "{0}". RC={1}'.format(
            data_set, rc
        )
        super(DatasetDeleteError, self).__init__(self.msg)

class DatasetCreateError(Error):
    def __init__(self, data_set, rc):
        self.msg = 'An error occurred during creation of data set "{0}". RC={1}'.format(
            data_set, rc
        )
        super(DatasetCreateError, self).__init__(self.msg)

def main():
    run_module()

if __name__ == '__main__':
    main()


