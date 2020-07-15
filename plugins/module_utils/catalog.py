
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import ( # pylint: disable=import-error
  DDStatement,
  FileDefinition,
  DatasetDefinition,
  StdoutDefinition,
  StdinDefinition,
  DummyDefinition,
  VIODefinition
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser # pylint: disable=import-error
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_raw import MVSCmd # pylint: disable=import-error
import tempfile
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.import_handler import ( # pylint: disable=import-error
  MissingZOAUImport,
) 
import tempfile
import pprint

class catalog():

    def __init__(self, module, result, parsed_args):
      self.module = module
      self.result = result
      self.parsed_args = parsed_args


    def execute_catalog_populate(self):
      self._constructCommonDDStatements()
      self._constructCatalogDDStatements()
      try:
        response = MVSCmd.execute("DFS3PU00", self.dDStatements, self.paramString, verbose=False)
        self.result["rc"] = response.rc
        self.result["content"] = response.stdout
        self.result["stderr"] = response.stderr
      except Exception as e:
        self.module.fail_json(msg=repr(e), **self.result)
      
      return self.result

    def execute_catalog_purge(self):
      self._constructCommonDDStatements()
      self._constructPurgeDDStatements()
      try:
        response = MVSCmd.execute("DFSRRC00", self.dDStatements, self.paramString, verbose=False)
        self.result["rc"] = response.rc
        self.result["content"] = response.stdout
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

      sysinList = self._parse_sysin()
      print("this is sysinList" + " ".join(sysinList))
      sysInDDStatement = DDStatement("SYSIN", StdinDefinition(sysinList))
      dDStatementList.append(sysInDDStatement)

      if self.parsed_args.get("delete") is not None:
        sysut1List = self._parse_sysut1()
        print("this is sysut1List" + " ".join(sysut1List))
        sysut1DDStatement = DDStatement("SYSUT1", StdinDefinition(sysut1List))
      else:
        if self.parsed_args.get("sysut1") is not None:
          sysut1DDStatement = DDStatement("SYSUT1", DatasetDefinition(**{k: v for k, v in self.parsed_args.get('sysut1').items() if v is not None}))
          # sysut1DDStatement = DDStatement("SYSUT1", StdoutDefinition())
        else:
          sysut1DDStatement = DDStatement("SYSUT1", StdoutDefinition())
      dDStatementList.append(sysut1DDStatement)
      
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
        
      if self.parsed_args.get('secondary_log_dataset') is not None:
        iefrder2DDStatement = DDStatement("IEFRDER2", DatasetDefinition(**{k: v for k, v in self.parsed_args.get('secondary_log_dataset').items() if v is not None}))
        dDStatementList.append(iefrder2DDStatement)
      
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
  
      #add sysabend dd statement
      if self.parsed_args.get('sysabend') is None:
        sysDefinition = StdoutDefinition()
      else:
        sysDefinition = DatasetDefinition(parsed_args['sysabend'])
      sysabendDDStatement = DDStatement("SYSABEND", sysDefinition)
      dDStatementList.append(sysabendDDStatement)
  
      controlList=[]
      if self.parsed_args.get('control_statements') is not None:
        print("getting control statements")
        controlList = self._parse_control_statements()
        ctrlStateDDStatement = DDStatement("SYSINP", StdinDefinition(controlList))
        dDStatementList.append(ctrlStateDDStatement)
        
      irlm_id = ""
      irlm_flag = "N"
      if self.parsed_args.get('irlm_enabled'):
        if self.parsed_args.get('irlm_id'):
          irlm_id = self.parsed_args.get('irlm_id')
          irlm_flag = "Y"
        else: 
          self.result['msg'] = "You must specify an irlm id"
          self.module.fail_json(**self.result)
      
      mode = ""
      mode_param = self.parsed_args.get('mode')
      if mode_param == 'LOAD':
        mode = 'DFSCPL00'
      elif mode_param == 'UPDATE':
        mode = "DFSCP001"
      elif mode_param == 'READ':
        mode = "DFSCP000"
  
      self.paramString = "DLI,DFS3PU00,{0},,,,,,,,,,,N,{1},{2},,,,,,,,,,,'DFSDF=CAT'".format(mode, irlm_flag, irlm_id)
      self.dDStatements = self.dDStatements + dDStatementList
  

    def _parse_control_statements(self):
        controlStatements = self.parsed_args.get('control_statements')
        controlStr=[]
        if controlStatements.get('print_duplicate_resources') is not None:
          if controlStatements.get('print_duplicate_resources') == True:
            controlStr.append("DUPLIST")
          else:
            controlStr.append("NODUPLIST")
        if controlStatements.get('max_error_msgs') is not None:
            controlStr.append("ERRORMAX="+ str(controlStatements['max_error_msgs']))
        if controlStatements.get('resource_chkp_freq') is not None:
            controlStr.append("RESOURCE_CHKP_FREQ="+str(controlStatements.get('resource_chkp_freq')))
        if controlStatements.get('segment_chkp_freq') is not None:
            controlStr.append("SEGMENT_CHKP_FREQ="+str(controlStatements.get('resource_chkp_freq')))
        if controlStatements.get('print_inserted_resources') is not None:
          if controlStatements.get('print_inserted_resources') == True:
            controlStr.append("ISRTLIST")
          else:
            controlStr.append("NOISRTLIST")

        managed_acbs=controlStatements.get('managed_acbs')
        if managed_acbs is not None:
          controlStr.append(self._parse_managed_acbs(managed_acbs))
        
        print("util printing control string: " + " ".join(controlStr))
        return controlStr
    
    def _parse_managed_acbs(self, managed_acbs):
        managed_acbs_string=[]
        managed_acbs_string.append("MANAGEDACBS=")
        if managed_acbs.get('setup') is not None:
          managed_acbs_string.append("SETUP")
          return "".join(managed_acbs_string)

        if managed_acbs.get('stage') is not None:
          managed_acbs_string.append("(STAGE")
          if managed_acbs.get('stage').get('gsamdbd') is not None:
            managed_acbs_string.append(",GSAM=" + managed_acbs.get('stage').get('gsamdbd'))
            return "".join(managed_acbs_string)
          if managed_acbs.get('stage').get('save_acb') is not None:
            managed_acbs_string.append("," + managed_acbs.get('stage').get('save_acb'))
          if managed_acbs.get('stage').get("clean_staging_set") is True:
            managed_acbs_string.append(",DELETE")
          if managed_acbs.get('stage').get('GSAMPCB') is True:
            managed_acbs_string.append(",GSAMPCB")
          managed_acbs_string.append(")")
          return "".join(managed_acbs_string)

        if managed_acbs.get('update') is not None:
          managed_acbs_string.append("(UPDATE")
          if managed_acbs.get('update').get('gsamdbd') is not None:
            managed_acbs_string.append(",GSAM=" + managed_acbs.get('stage').get('gsamdbd'))
            return "".join(managed_acbs_string)
          if managed_acbs.get('update').get('replace_acb') is not None:
            managed_acbs_string.append("," + managed_acbs.get('update').get('replace_acb'))
          if managed_acbs.get('update').get("share_mode") is True:
            managed_acbs_string.append(",SHARE")
          if managed_acbs.get('update').get('GSAMPCB') is True:
            managed_acbs_string.append(",GSAMPCB")
          managed_acbs_string.append(")")
          return "".join(managed_acbs_string)


    def _parse_sysin(self):
      sysinList = []
      if self.parsed_args.get("mode") is not None:
        modeString = "MODE " + self.parsed_args.get("mode")
        sysinList.append(modeString)
      if self.parsed_args.get("delete_dbd_by_version") is not None and self.parsed_args.get("mode") != "PURGE":
        deldbverList = self.parsed_args.get("delete_dbd_by_version")
        for deld in deldbverList:
          deldbverString = ['DELDBVER']
          if deld.get("member_name") is not None:
            deldbverString.append(deld.get("member_name"))
          if deld.get("version_number") is not None:
            deldbverString.append(str(deld.get("version_number")))
          sysinList.append(" ".join(deldbverString))
      if self.parsed_args.get("update_retention_criteria") is not None:
        updateList = self.parsed_args.get("update_retention_criteria")
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
      if self.parsed_args.get("managed_acbs") is not None:
        sysinList.append("MANAGEDACBS UPDATE")
      if self.parsed_args.get("resource_chkp_freq") is not None:
        sysinList.append("RESOURCE_CHKP_FREQ " + str(self.parsed_args.get("resource_chkp_freq")))
          
      return sysinList
    
    def _parse_sysut1(self):
      sysut1List = []
      if self.parsed_args.get("delete_dbd_by_version") is not None and self.parsed_args.get("MODE") == "PURGE":
        deldbverList = self.parsed_args.get("delete_dbd_by_version")
        for deld in deldbverList:
          deldbverString = ['DELDBVER']
          if deld.get("member_name") is not None:
            deldbverString.append(deld.get("member_name"))
          if deld.get("version_number") is not None:
            deldbverString.append(str(deld.get("version_number")))
          sysut1List.append(" ".join(deldbverString))
      if self.parsed_args.get("delete") is not None:
        deleteList = self.parsed_args.get("delete")
        for dele in deleteList:
          deleteString = ["DELETE"]
          if dele.get("resource") is not None:
            deleteString.append(dele.get("resource"))
          if dele.get("member_name") is not None:
            deleteString.append(dele.get("member_name"))
          if dele.get("time_stamp") is not None:
            deleteString.append(dele.get("time_stamp"))
          sysut1List.append(" ".join(deleteString))
      
      return sysut1List


 

# def ims_resource(resource_name, dependencies): 
#   if len(resource_name) > 8 and not isinstance(resource_name, str):
#     raise ValueError('The resource name cannot be more than 8 characters')
#   return resource_name