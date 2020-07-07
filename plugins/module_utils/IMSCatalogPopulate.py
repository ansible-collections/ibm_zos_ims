
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import ( # pylint: disable=import-error
  DDStatement,
  FileDefinition,
  DatasetDefinition,
  StdoutDefinition,
  StdinDefinition,
  DummyDefinition
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser # pylint: disable=import-error
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_raw import MVSCmd # pylint: disable=import-error
import tempfile
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.import_handler import ( # pylint: disable=import-error
  MissingZOAUImport,
) 
import tempfile
import pprint

class IMSCatalogPopulate():

    def __init__(self, module):
      self.module = module
      self.params = module.params
      self.result = {}
      self._validate_common_input()


    def execute_catalog_populate(self):
      self._validate_populate_input()
      self._constructCommonDDStatements()
      self._constructCatalogDDStatements()
      try:
        response = MVSCmd.execute("DFS3PU00", self.dDStatements, self.paramString, verbose=True)
        self.result["rc"] = response.rc
        self.result["stdout"] = response.stdout
        self.result["stderr"] = response.stderr
      except Exception as e:
        self.module.fail_json(msg=repr(e), **self.result)
      
      return self.result

    def execute_catalog_purge(self):
      self._validate_purge_input()
      self._constructCommonDDStatements()
      self._constructPurgeDDStatements()
      try:
        response = MVSCmd.execute("DFSRRC00", self.dDStatements, self.paramString, verbose=True)
        self.result["rc"] = response.rc
        self.result["stdout"] = response.stdout
        self.result["stderr"] = response.stderr
      except Exception as e:
        self.module.fail_json(msg=repr(e), **self.result)
      
      return self.result

    def _constructCommonDDStatements(self):
      #DD statement Generation
      dDStatementList = []
      imsDatasetList = []
  
      if self.parsed_args.get('reslib') is not None:
        dfsreslbDDStatement = DDStatement("DFSRESLB", DatasetDefinition(self.parsed_args.get('reslib')))
        dDStatementList.append(dfsreslbDDStatement)
      if self.parsed_args.get('buffer_pool_param_dataset') is not None:
        dfsvsampDDStatement = DDStatement("DFSVSAMP", DatasetDefinition(self.parsed_args.get('buffer_pool_param_dataset')))
        dDStatementList.append(dfsvsampDDStatement)
      if self.parsed_args.get('primary_log_dataset') is not None:
        iefrderDDStatement = DDStatement("IEFRDER", DatasetDefinition(**{k: v for k, v in self.parsed_args.get('primary_log_dataset').items() if v is not None}))
        dDStatementList.append(iefrderDDStatement)
    
      #Generate DD statements for DBD and PSB libs. If they exist, we attach to an ims dd statement. 
      if self.parsed_args.get('psb_lib') is not None:
        psbDataset = DatasetDefinition(self.parsed_args.get('psb_lib'))
        imsDatasetList.append(psbDataset)
      if self.parsed_args.get('dbd_lib') is not None:
        dbdDatset = DatasetDefinition(self.parsed_args.get('dbd_lib'))
        imsDatasetList.append(dbdDatset)
      if imsDatasetList is not None:
        imsDDStatement = DDStatement("IMS", imsDatasetList)
        dDStatementList.append(imsDDStatement)
      if self.parsed_args.get('proclib') is not None:
        proclibDDStatement = DDStatement("PROCLIB", DatasetDefinition(self.parsed_args.get('proclib')))
        dDStatementList.append(proclibDDStatement)
  
      if self.parsed_args.get('steplib') is not None:
        steplibDDStatement = DDStatement("STEPLIB", DatasetDefinition(self.parsed_args.get('steplib')))
        dDStatementList.append(steplibDDStatement)
  
      #Add sysprint dd statement
      if self.parsed_args.get('sysprint') is None:
        sysDefinition = StdoutDefinition()
      else:
        sysDefinition = DatasetDefinition(self.parsed_args.get('sysprint'))
      sysprintDDStatement = DDStatement("SYSPRINT", sysDefinition)
      dDStatementList.append(sysprintDDStatement)

      self.dDStatements = dDStatementList

    def _constructPurgeDDStatements(self):
      dDStatementList = []

      if self.parsed_args.get("sysin") is not None:
        sysinList = self._parse_sysin()
        sysInDDStatement = DDStatement("SYSIN", StdinDefinition(sysinList))
      dDStatementList.append(sysInDDStatement)

      if self.parsed_args.get("sysut1") is not None:
        sysut1List = self._parse_sysut1()
        sysut1DDStatement = DDStatement("SYSUT1", StdinDefinition(sysut1List))
      dDStatementList.append(sysut1DDStatement)

      self.dDStatements = self.dDStatements + dDStatementList
      
      irlm_id = ""
      irlm_flag = "N"
      if self.parsed_args.get('irlm_enabled'):
        if self.parsed_args.get('irlm_id'):
          irlm_id = self.parsed_args.get('irlm_id')
          irlm_flag = "Y"
        else: 
          self.result['msg'] = "You must specify an irlm id"
          self.module.fail_json(**self.result)
  
      self.paramString = "DLI,DFS3PU10,DFSCP001,,,,,,,,,,,N,{0},{1},,,,,,,,,,,'DFSDF=CAT'".format(irlm_flag, irlm_id)
      self.dDStatements = self.dDStatements + dDStatementList
  


    def _constructCatalogDDStatements(self):
      dDStatementList = []
      acbDatasetList = []

      #Generate DD statements for ACB lib. Behavior is different depending on check_timestamps
      if self.parsed_args.get('acb_lib') is not None:
        #Check if check_timestamp is false. If so, then we include all the datasets in a single DD Statement
        if self.parsed_args.get('check_timestamp') is False:
          for i in self.parsed_args.get('acb_lib'):
            acbDataset = DatasetDefinition(i)
            acbDatasetList.append(acbDataset)
          acbDDStatement = DDStatement("IMSACBA", acbDatasetList)
          dDStatementList.append(acbDDStatement)
        #If check_timestamp is true, then we generate a dd statement for each dataset
        else:
          acbCount = 1
          for i in self.parsed_args.get('acb_lib'):
            if acbCount >= 10:
              acbDDStatement = DDStatement("IMSACB{0}".format(acbCount), DatasetDefinition(i))
              dDStatementList.append(acbDDStatement)
              acbCount += 1
            else:
              acbDDStatement = DDStatement("IMSACB0{0}".format(acbCount), DatasetDefinition(i))
              dDStatementList.append(acbDDStatement)
              acbCount += 1
          acbCount = 1
        
      if self.parsed_args.get('bootstrap_dataset') is not None:
        btstrDataset = DDStatement("IMSDBSDS", DatasetDefinition(self.parsed_args.get('bootstrap_dataset')))
        dDStatementList.append(btstrDataset)
      
      if self.parsed_args.get('directory_datasets') is not None:
        directoryCount = 1
        for i in self.parsed_args.get('directory_datasets'):
          if acbCount >= 10:
            directoryDDStatement = DDStatement("IMSD00{0}".format(directoryCount), DatasetDefinition(i))
            dDStatementList.append(directoryDDStatement)
          else:
            directoryDDStatement = DDStatement("IMSD000{0}".format(directoryCount), DatasetDefinition(i))
            dDStatementList.append(directoryDDStatement)
      
      if self.parsed_args.get('temp_acb_dataset') is not None:
        tempDDStatement = DDStatement("IMSDG001", DatasetDefinition(self.parsed_args.get('temp_acb_dataset')))
        dDStatementList.append(tempDDStatement)
      
      if self.parsed_args.get('directory_staging_dataset') is not None:
        dirDDStatement = DDStatement("IMDSTAG", DatasetDefinition(self.parsed_args.get('directory_staging_dataset')))
        dDStatementList.append(dirDDStatement)
  
      #Add dummy dd statement
      dummyDDStatement = DDStatement("ACBCATWK", DummyDefinition())
      dDStatementList.append(dummyDDStatement)
  
      # #add sysabend dd statement
      # if parsed_args.get('sysabend') is None:
      #   sysDefinition = StdoutDefinition()
      # else:
      #   sysDefinition = DatasetDefinition(parsed_args['sysabend'])
      # sysabendDDStatement = DDStatement("SYSABEND", sysDefinition)
      # dDStatementList.append(sysabendDDStatement)
  
      # controlList=[]
      # if parsed_args.get('control_statements') is not None:
      #   print("getting control statements")
      #   controlList = parse_control_statements(parsed_args.get('control_statements'))
      # ctrlStateDDStatement = DDStatement("SYSINP", StdinDefinition(controlList))
      # dDStatementList.append(ctrlStateDDStatement)
        
      irlm_id = ""
      irlm_flag = "N"
      if self.parsed_args.get('irlm_enabled'):
        if self.parsed_args.get('irlm_id'):
          irlm_id = self.parsed_args.get('irlm_id')
          irlm_flag = "Y"
        else: 
          self.result['msg'] = "You must specify an irlm id"
          self.module.fail_json(**self.result)
  
      self.paramString = "DLI,DFS3PU00,DFSCP001,,,,,,,,,,,N,{0},{1},,,,,,,,,,,'DFSDF=CAT'".format(irlm_flag, irlm_id)
      self.dDStatements = self.dDStatements + dDStatementList
  

    def _validate_common_input(self):
        try:
          module_defs = dict(
            irlm_enabled=dict(arg_type="bool", required=False),
            irlm_id=dict(arg_type="str", required=False),
            reslib=dict(arg_type="data_set", required=False),
            buffer_pool_param_dataset=dict(arg_type="data_set", required=False),
            primary_log_dataset=dict(arg_type="dict", 
              options=dict(
                dataset_name=dict(arg_type="data_set", required=True),
                 disposition=dict(arg_type="str", required=False, choices=['EXCL','OLD','SHR','NEW']),
                 primary=dict(arg_type="int", required=False),
                 primary_unit=dict(arg_type="str", required=False, choices=['K', 'KB', 'M', 'MB', 'G', 'GB', 'C', 'CYL', 'T', 'TRK']),
                 secondary=dict(arg_type="int", required=False),
                 secondary_unit=dict(arg_type="str", required=False, choices=['K', 'KB', 'M', 'MB', 'G', 'GB', 'C', 'CYL', 'T', 'TRK']),
                 normal_disposition=dict(arg_type="str", required=False, choices=['KEEP', 'DELETE', 'CATLG', 'UNCATLG']),
                 conditional_disposition=dict(arg_type="str", required=False, choices=['KEEP', 'DELETE', 'CATLG', 'UNCATLG']),
                 record_format=dict(arg_type="str", required=False, choices=['FB', 'VB', 'FBA', 'VBA', 'U']),
                 record_length=dict(arg_type="int", required=False),
                 block_size=dict(arg_type="int", required=False),
                 type = dict(arg_type="str", required=False, choices=['SEQ','BASIC','LARGE','PDS','PDSE','LIBRARY','LDS','RRDS','ESDS','KSDS'])
              ),
              required=False),
            psb_lib=dict(arg_type="data_set", required = False),
            dbd_lib=dict(arg_type="data_set", required = False),
            proclib=dict(arg_type="data_set", required = False),
            steplib=dict(arg_type="data_set", required = False),
            sysprint=dict(arg_type="data_set", required=False),
            check_timestamp=dict(arg_type="bool", required=False)
          )

          parser = BetterArgParser(module_defs)
          self.parsed_args = parser.parse_args(self.params)

        except ValueError as error:
          self.result['msg'] = error.args
          self.result['rc']=1
          self.module.fail_json(**self.result)

    def _validate_populate_input(self):
        try:
          module_defs = dict(
            secondary_log_dataset=dict(arg_type="dict", 
              options=dict(
                dataset_name=dict(arg_type="data_set", required=True),
                disposition=dict(arg_type="str", required=False, choices=['EXCL','OLD','SHR','NEW']),
                primary=dict(arg_type="int", required=False),
                primary_unit=dict(arg_type="str", required=False, choices=['K', 'KB', 'M', 'MB', 'G', 'GB', 'C', 'CYL', 'T', 'TRK']),
                secondary=dict(arg_type="int", required=False),
                secondary_unit=dict(arg_type="str", required=False, choices=['K', 'KB', 'M', 'MB', 'G', 'GB', 'C', 'CYL', 'T', 'TRK']),
                normal_disposition=dict(arg_type="str", required=False, choices=['KEEP', 'DELETE', 'CATLG', 'CATALOG', 'UNCATLG']),
                conditional_disposition=dict(arg_type="str", required=False, choices=['KEEP', 'DELETE', 'CATLG', 'CATALOG', 'UNCATLG']),
                record_format=dict(arg_type="str", required=False, choices=['FB', 'VB', 'FBA', 'VBA', 'U']),
                record_length=dict(arg_type="int", required=False),
                block_size=dict(arg_type="int", required=False)
              ), 
              required=False),
            acb_lib=dict(arg_type="list", elements="data_set", required=True),
            bootstrap_dataset=dict(arg_type="data_set", required = False),
            directory_datasets=dict(arg_type="list", elements="data_set", required=False),
            temp_acb_dataset=dict(arg_type="data_set", required = False),
            directory_staging_dataset=dict(arg_type="data_set", required = False),
            sysabend=dict(arg_type="data_set", required = False),
            control_statements=dict(arg_type="dict", 
              options=dict(
                duplist=dict(arg_type="bool", required=False),
                  errormax=dict(arg_type="int", required=False),
                  resource_chkp_freq=dict(arg_type="int", required=False),
                  segment_chkp_freq=dict(arg_type="int", required=False),
                  isrtlist=dict(arg_type="bool", required=False),
                  managed_acbs=dict(arg_type="dict", 
                    required=False, 
                    options=dict(
                      setup=dict(arg_type="bool", required=False),
                      stage=dict(arg_type=dict, required=False, 
                        options=dict(
                          latest=dict(arg_type="bool", required=False),
                          uncond=dict(arg_type="bool", required=False),
                          delete=dict(arg_type="bool", required=False),
                          gsampcb=dict(arg_type="bool", required=False),
                          gsamdbd=dict(arg_type="str", required=False)
                        )
                      ),
                      update=dict(arg_type=dict, required=False, 
                        options=dict(
                          latest=dict(arg_type="bool", required=False),
                          uncond=dict(arg_type="bool", required=False),
                          share=dict(arg_type="bool", required=False),
                          gsampcb=dict(arg_type="bool", required=False),
                          gsamdbd=dict(arg_type="str", required=False)
                        )
                      )
                    )
                  ),
                no_isrtlist=dict(arg_type="bool", required=False)
              ),
              required=False)
          )

          parser = BetterArgParser(module_defs)
          self.parsed_args.update(parser.parse_args(self.params))

          if self.parsed_args.get('directory_staging_dataset') is not None:
            self.directory_datasets = self.parsed_args.get('directory_datasets')
            self._validate_directory_staging_dataset()

        except ValueError as error:
          self.result['msg'] = error.args
          self.result['rc']=1
          self.module.fail_json(**self.result)
    
    def _validate_purge_input(self):
        try:
          module_defs = dict(
            sysin=dict(arg_type="dict", required=True,
              options=dict(
                mode=dict(arg_type="str", required=True),
                deldbver=dict(arg_type="list", elements="dict", required=False,
                  options=dict(
                    member_name=dict(arg_type="str", required=True),
                    version_number=dict(arg_type="int", required=True)
                  )
                ),
                update=dict(arg_type="list", elements="dict", required=False,
                  options=dict(
                    resource=dict(arg_type="str", required=True, choices=['DBD', 'PSB']),
                    member_name=dict(arg_type="str", required=True),
                    instances=dict(arg_type="int", required=True),
                    days=dict(arg_type="int", required=False)
                  )
                )
              )
            ),
            sysut1=dict(arg_type="dict", required=False,
              options=dict(
                deldbver=dict(arg_type="list", elements="dict", required=False,
                  options=dict(
                    member_name=dict(arg_type="str", required=True),
                    version_number=dict(arg_type="int", required=True)
                  )
                ),
                delete=dict(arg_type="list", elements="dict", required=False,
                  options=dict(
                    resource=dict(arg_type="str", required=True, choices=['DBD', 'PSB']),
                    member_name=dict(arg_type="str", required=True),
                    time_stamp=dict(arg_type="int", required=False)
                  )
                )
              )
            )
          )

          parser = BetterArgParser(module_defs)
          self.parsed_args.update(parser.parse_args(self.params))
        
        except ValueError as error:
          self.result['msg'] = error.args
          self.result['rc']=1
          self.module.fail_json(**self.result)


    def _validate_directory_staging_dataset(self):
        if len(self.directory_datasets) > 20:
          self.result['msg'] = "You cannot specify more than 20 IMS directory datasets"
          self.module.fail_json(**self.result)


    def _parse_control_statements(self):
        controlStatements = self.params.get('control_statements')
        controlStr=[]
        if controlStatements.get('duplist') is not None:
            controlStr.append("DUPLIST")
        if controlStatements.get('errormax') is not None:
            controlStr.append("ERRORMAX="+ str(controlStatements['errormax']))
        if controlStatements.get('resource_chkp_freq') is not None:
            controlStr.append("RESOURCE_CHKP_FREQ="+str(controlStatements.get('resource_chkp_freq')))
        if controlStatements.get('segment_chkp_freq') is not None:
            controlStr.append("SEGMENT_CHKP_FREQ="+str(controlStatements.get('resource_chkp_freq')))
        if controlStatements.get('isrtlist') is not None:
            controlStr.append("ISRTLIST")
        if controlStatements.get('no_isrtlist') is not None:
            controlStr.append("NOISRTLIST")

        managed_acbs_string=[]
        managed_acbs=controlStatements.get('managed_acbs')
        if managed_acbs is not None:
          managed_acbs_string.append("MANAGEDACBS=")
          if managed_acbs.get('setup') is not None:
            managed_acbs_string.append("SETUP")
            controlStr.append("".join(managed_acbs_string))
            print("util printing control string: " + " ".join(controlStr))
            return controlStr
          if managed_acbs.get('stage') is not None:
            managed_acbs_string.append("STAGE")
            if managed_acbs.get('stage').get('gsamdbd') is not None:
              managed_acbs_string.append(",GSAM=" + managed_acbs.get('stage').get('gsamdbd'))
            if managed_acbs.get('stage').get('latest') is not None:
              managed_acbs_string.append(",LATEST")
            elif managed_acbs.get('stage').get("uncond") is not None:
              managed_acbs_string.append(",UNCOND")
            if managed_acbs.get('stage').get("delete") is not None:
              managed_acbs_string.append(",DELETE")
            if managed_acbs.get('stage').get('GSAMPCB') is not None:
              managed_acbs_string.append(",GSAMPCB")
            controlStr.append("".join(managed_acbs_string))
            print("util printing control string: " + " ".join(controlStr))
            return controlStr
          if managed_acbs.get('update') is not None:
            managed_acbs_string.append("UPDATE")
            if managed_acbs.get('update').get('gsamdbd') is not None:
              managed_acbs_string.append(",GSAM=" + managed_acbs.get('stage').get('gsamdbd'))
            if managed_acbs.get('update').get('latest') is not None:
              managed_acbs_string.append(",LATEST")
            elif managed_acbs.get('update').get("uncond") is not None:
              managed_acbs_string.append(",UNCOND")
            if managed_acbs.get('update').get("share") is not None:
              managed_acbs_string.append(",SHARE")
            if managed_acbs.get('update').get('GSAMPCB') is not None:
              managed_acbs_string.append(",GSAMPCB")
            controlStr.append("".join(managed_acbs_string))
            print("util printing control string: " + controlStr)
            return controlStr

        controlStr.append("".join(managed_acbs_string))
        print("util printing control string: " + " ".join(controlStr))
        return controlStr

    def _parse_sysin(self):
      sysinStatements = self.params.get("sysin")
      sysinList = []
      if sysinStatements.get("mode") is not None:
        modeString = "MODE " + sysinStatements.get("mode")
        sysinList.append(modeString)
      if sysinStatements.get("deldbver") is not None:
        deldbverList = sysinStatements.get("deldbver")
        for deld in deldbverList:
          deldbverString = ['DELDBVER']
          if deld.get("member_name") is not None:
            deldbverString.append(deld.get("member_name"))
          if deld.get("version_number") is not None:
            deldbverString.append(str(deld.get("version_number")))
          sysinList.append(" ".join(deldbverString))
      if sysinStatements.get("update") is not None:
        updateList = sysinStatements.get("update")
        for upd in updateList:
          updateString = ['UPDATE']
          if upd.get("resource") is not None:
            updateString.append(upd.get("resource"))
          if upd.get("member_name") is not None:
            updateString.append(upd.get("member_name"))
          if upd.get("instances") is not None:
            updateString.append(str(upd.get("instances")))
          if upd.get("days") is not None:
            updateString.append(str(upd.get("days")))
          sysinList.append(" ".join(updateString))
          
      return sysinList
    
    def _parse_sysut1(self):
      sysut1Statements = self.params.get("sysut1")
      sysut1List = []
      if sysut1Statements.get("deldbver") is not None:
        deldbverList = sysut1Statements.get("deldbver")
        for deld in deldbverList:
          deldbverString = ['DELDBVER']
          if deld.get("member_name") is not None:
            deldbverString.append(deld.get("member_name"))
          if deld.get("version_number") is not None:
            deldbverString.append(str(deld.get("version_number")))
          sysut1List.append(" ".join(deldbverString))
      if sysut1Statements.get("delete") is not None:
        deleteList = sysut1Statements.get("delete")
        for dele in deleteList:
          deleteString = ["DELETE"]
          if dele.get("resource") is not None:
            deleteString.append(dele.get("resource"))
          if dele.get("member_name") is not None:
            deleteString.append(dele.get("member_name"))
          if dele.get("time_stamp") is not None:
            deleteString.append(str(dele.get("time_stamp")))
          sysut1List.append(" ".join(deleteString))
      
      return sysut1List


 

# def ims_resource(resource_name, dependencies): 
#   if len(resource_name) > 8 and not isinstance(resource_name, str):
#     raise ValueError('The resource name cannot be more than 8 characters')
#   return resource_name