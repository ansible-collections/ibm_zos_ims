from __future__ import (absolute_import, division, print_function)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import (  # pylint: disable=import-error
    DDStatement,
    DatasetDefinition,
    StdoutDefinition,
    StdinDefinition,
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd  # pylint: disable=import-error
import re

from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.ims_module_error_messages import ZDDLErrorMessages as em  # pylint: disable=import-error

__metaclass__ = type


class zddl(object):
    ZDDL_UTILITY = "DFS3ID00"
   

    def __init__(self, sql_input, online, ims_id, irlm_id, reslib, steplib, proclib, control_statements):
        """IMSzDDL constructor for generating IMS zDDL using zos_mvs_raw
        Args:
           sql_input (list): command input to specify.
           online (bool): indicates if its BMP or DL/I.
           ims_id (str): the id of the IMS system on which job is to be run.
           irlm_id (str): The irlm id if irlm is enabled.
           reslib (list): List of reslib datasets.
           proclib (list): List of proclib datasets.
           steplib (list): Points to the list of IMS SDFSRESL data set, which contains the IMS nucleus and required IMS modules.
           control_statements (dict): The control statement parameters.
        """
        self.online = online
        self.ims_id = ims_id
        self.irlm_id = irlm_id
        self.reslib = reslib
        self.proclib = proclib
        self.steplib = steplib
        self.sql_input = sql_input
        self.control_statements = control_statements
       
        self._assert_valid_input_types()
        self.result = {}

    def _assert_valid_input_types(self):
        """This assertion function validates that all parameters are the correct data type.
         Raises:
              TypeError: Raised if parameter is the wrong data type.
        """
        # if self.online and not isinstance(self.online, bool):
        #     raise TypeError(em.INCORRECT_ONLINE_TYPE)
        if self.ims_id and not isinstance(self.ims_id, str):
            raise TypeError(em.INCORRECT_IMS_ID_TYPE)
        # if self.irlm_id and not isinstance(self.irlm_id, str):
        #     raise TypeError(em.INCORRECT_IRLM_ID_TYPE)
        if self.reslib and not all(isinstance(item, str) for item in self.reslib):
            raise TypeError(em.INCORRECT_RESLIB_TYPE)
        if self.steplib and not all(isinstance(item, str) for item in self.steplib):
            raise TypeError(em.INCORRECT_STEPLIB_TYPE)
        if self.proclib and not all(isinstance(item, str) for item in self.proclib):
            raise TypeError(em.INCORRECT_PROCLIB_TYPE)    
        # if self.sql_input and not all(isinstance(item, str) for item in self.sql_input):
        #     raise TypeError(em.INCORRECT_SQL_INPUT_TYPE) 

        if self.control_statements and not all(isinstance(item, str) for item in self.control_statements):
            raise TypeError(em.INCORRECT_CONTROL_STATEMENTS_TYPE)

    def _build_zddl_statements(self):
        """Builds the list of DDStatements that will be provided to the zos_mvs_raw to execute DFS3ID00
         based on the user input.

        Returns:
          (list[DDStatement]): List of DDStatements
        """
        zddl_utility_fields = []
        # ims_dataset_list = []
        sysprint = DDStatement("SYSPRINT", StdoutDefinition())

        zddl_utility_fields.append(sysprint)

        if self.steplib:
            steplib_data_set_definitions = [
                DatasetDefinition(steplib) for steplib in self.steplib]
            steplib = DDStatement("STEPLIB", steplib_data_set_definitions)
            zddl_utility_fields.append(steplib)

        if self.reslib:
            reslib = self.reslib
        else:
            reslib = self.steplib

        if self.reslib:
            reslib_data_set_definitions = [
                DatasetDefinition(reslib) for reslib in self.reslib]
            reslib_dd_statement = DDStatement("DFSRESLB", reslib_data_set_definitions)
            zddl_utility_fields.append(reslib_dd_statement)

        if self.proclib:
            proclib_data_set_definitions = [
                DatasetDefinition(proclib) for proclib in self.proclib]
            proclib = DDStatement("PROCLIB", proclib_data_set_definitions)
            zddl_utility_fields.append(proclib)


        print("Hello")
        print("online: ")
        print(type(self.online))
        print("irlm_id: ")
        print(type(self.irlm_id))
        print("sql_input: ")
        print(type(self.sql_input))

        sql_input_list = []
        if self.sql_input is not None:

            for command in self.sql_input:
                sql_input_list.append(command)
            for a in sql_input_list:
                print("sql_input_list: ", a)

        command_imssql_definition = DDStatement(
            "IMSSQL", StdinDefinition("\n".join(sql_input_list))
        )

        zddl_utility_fields.append(command_imssql_definition)

        return zddl_utility_fields

    # def _split_lines_command(self):
    #     """Splitting the command on new line in case if it exceeds 72 characters.

    #     Returns: A string or array of Sql commands.
    #     """
    #     return_str = ""
    #     return_arr = []
    #     psbnames = self.psb_name
    #     if len(psbnames) < 6:
    #         return_str = self._build_psb_name_string(
    #             self.command_input, psbnames)
    #         return return_str
    #     else:
    #         for i in range(0, len(psbnames), 5):
    #             new_psb_names_five = psbnames[i: i + 5]
    #             psb_line = self._build_psb_name_string(
    #                 self.command_input, new_psb_names_five)
    #             return_arr.append(psb_line)
    #         return "\n ".join(return_arr)
    #     return return_arr


    def combine_results(self, result):
        """Add results of execution to existing
        results if there are any.

        Args:
            result ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self.result is None:
            self.result = {}
        self.result['rc'] = max(self.result.get("rc", -1), result.rc)
        self.result["output"] = self.result.get("output", "") + result.stdout
        self.result["error"] = self.result.get("error", "") + result.stderr
        return self.result


    def execute(self):
        """Executes the DATA DEFINITION utility DFSRRC00 using the zos_mvs_raw module based on the user input.

        Returns:
          (dict): (1) rc:      Return Code returned by zos_mvs_raw module.
                  (2) error:   The stderr returned by the zos_raw module.
                  (3) output:  The original output provided by zos_raw.
        """
        self.result = {}
        response = None
    
        zddl_utility_fields = self._build_zddl_statements()
        response = MVSCmd.execute(
            ZDDL_UTILITY, zddl_utility_fields, verbose=True)
        self.result = self.combine_results(response)
      
        return self.result
