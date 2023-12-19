from __future__ import (absolute_import, division, print_function)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import (  # pylint: disable=import-error
    DDStatement,
    DatasetDefinition,
    StdoutDefinition
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmd  # pylint: disable=import-error

from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.ims_module_error_messages import ZDDLErrorMessages as em  # pylint: disable=import-error

__metaclass__ = type


class zddl(object):
    ZDDL_UTILITY = "DFS3ID00"

    def __init__(self, online, ims_id, reslib, steplib, proclib, sql_input, verbose, auto_commit, simulate, dynamic_programview):
        """IMSzDDL constructor for generating IMS zDDL using zos_mvs_raw
        Args:
           sql_input (str): command input to specify.
           online (bool): indicates if its BMP or DL/I.
           ims_id (str): the id of the IMS system on which job is to be run.
           reslib (list): List of reslib datasets.
           proclib (list): List of proclib datasets.
           steplib (list): Points to the list of IMS SDFSRESL data set, which contains the IMS nucleus and required IMS modules.
           verbose (bool): Specifies if the utility will print full text of the DDL statements in the job log.
           auto_commit (bool): Specifies if the utility will perform auto Commit.
           simulate (bool): Specifies if the utility will perform simulation of DDL statements.
           dynamic_programview (bool): Specifies if the utility will automatically Import all the input CREATE PROGRAMVIEWs.
        """
        self.online = online
        self.ims_id = ims_id
        # self.irlm_id = irlm_id
        self.reslib = reslib
        self.steplib = steplib
        self.proclib = proclib
        self.sql_input = sql_input
        self.verbose = verbose
        self.auto_commit = auto_commit
        self.simulate = simulate
        self.dynamic_programview = dynamic_programview

        self._assert_valid_input_types()
        self.result = {}

    def _assert_valid_input_types(self):
        """This assertion function validates that all parameters are the correct data type.
         Raises:
              TypeError: Raised if parameter is the wrong data type.
        """
        if self.online and not isinstance(self.online, bool):
            raise TypeError(em.INCORRECT_ONLINE_TYPE)
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
        if self.sql_input and not isinstance(self.sql_input, str):
            raise TypeError(em.INCORRECT_SQL_INPUT_TYPE)
        if self.verbose and not isinstance(self.verbose, bool):
            raise TypeError(em.INCORRECT_VERBOSE_TYPE)
        if self.auto_commit and not isinstance(self.auto_commit, bool):
            raise TypeError(em.INCORRECT_AUTO_COMMIT_TYPE)
        if self.simulate and not isinstance(self.simulate, bool):
            raise TypeError(em.INCORRECT_SIMULATE_TYPE)
        if self.dynamic_programview and not isinstance(self.dynamic_programview, bool):
            raise TypeError(em.INCORRECT_DYNAMIC_PROGRAMVIEW)

    def _build_zddl_statements(self):
        """Builds the list of DDStatements that will be provided to the zos_mvs_raw to execute DFS3ID00
         based on the user input.

        Returns:
          (list[DDStatement]): List of DDStatements
        """
        zddl_utility_fields = []

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

        if self.sql_input:
            sql_input_data_set_definitions = DDStatement(
                "IMSSQL", DatasetDefinition(self.sql_input, disposition="old"))
            zddl_utility_fields.append(sql_input_data_set_definitions)
        sysprint = DDStatement("SYSPRINT", StdoutDefinition())
        zddl_utility_fields.append(sysprint)
        return zddl_utility_fields

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
        # self.result["output"] = self.result.get("output", "") + result.stdout
        # self.result['unformatted'] = result.stdout
        self.result['content'] = result.stdout.split("\n")
        self.result["error"] = self.result.get("error", "") + result.stderr

        return self.result

    def execute(self):
        """Executes the DATA DEFINITION utility DFS3ID00 using the mvscommand module based on the user input.

        Returns:
          (dict): (1) rc:      Return Code returned by mvscommand module.
                  (2) error:   The stderr returned by the mvscommand module.
                  (3) output:  The original output provided by mvscommand.
        """
        self.result = {}
        response = None
        if self.ims_id:
            param_string = "BMP,DFS3ID00,DFSCP001,,,,,,,,,,," + self.ims_id
            zddl_utility_fields = self._build_zddl_statements()
            # mvs_auth to be true
            response = MVSCmd.execute_authorized(
                zddl.ZDDL_UTILITY, zddl_utility_fields, param_string, verbose=False)
            self.result = self.combine_results(response)
        return self.result
