import re
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.dd_statement import ( # pylint: disable=import-error
  DDStatement,
  FileDefinition,
  DatasetDefinition,
  StdoutDefinition,
  StdinDefinition
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_raw import MVSCmd # pylint: disable=import-error
import tempfile
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.import_handler import ( # pylint: disable=import-error
  MissingZOAUImport,
) 

try:
  from zoautil_py import Datasets, types # pylint: disable=import-error
except Exception:
  Datasets = MissingZOAUImport()
  types = MissingZOAUImport()

class IMSDbrc():
    replacement_values = {
        "** NONE **": None,
        "**NULL**": None,
        "NONE": None,
        "YES": True,
        "NO": False,
        "ON": True,
        "OFF": False
    }

    def __init__(self, commands, steplib, dynalloc=None, dbdlib=None, genjcl=None, recon1=None, recon2=None, recon3=None):
        """DBRC object used to create and run DBRC commands using zos_raw.

        Args:
            commands (str, list[str]): List of the DBRC commands to be executed.
            steplib (str, list[str]): List of STEPLIB datasets that contain the IMS nucleus and the
                required action modules.
            dynalloc (str, optional): The DYNALLOC data set that will be used to complete the DBRC
                execution. Required if 'recon1', 'recon2', and 'recon3' are not specified. Defaults to None.
            dbdlib (str, optional): The data set that contains the database descriptions for the databases
                that are under the control of DBRC. Defaults to None.
            genjcl (str, optional): The PDS, which contains the JCL and control statements for the utility
                that DBRC uses to generate a job. Defaults to None.
            recon1 (str, optional): The RECON1 data set that will be used to complete the DBRC execution.
                Defaults to None. Required if 'dynalloc' is not specified.
            recon2 (str, optional): The RECON2 data set that will be used to complete the DBRC execution.
                Defaults to None. Required if 'dynalloc' is not specified.
            recon3 (str, optional): The RECON3 data set that will be used to complete the DBRC execution.
                Defaults to None. Required if 'dynalloc' is not specified.
        """
        self.commands = commands
        self.steplib_list = steplib
        self.dynalloc = dynalloc
        self.dbdlib = dbdlib
        self.genjcl = genjcl
        self.recon1 = recon1
        self.recon2 = recon2
        self.recon3 = recon3
        self._assert_valid_inputs()

    def _assert_valid_inputs(self):
        """Validates the data types and requirements to run DBRC commands.
        """
        self._assert_valid_input_types()
        self._assert_dynalloc_recon_requirement()

    def _assert_dynalloc_recon_requirement(self):
        """This assertion function validates that either the 'dynalloc' parameter was specified, or 
        all of the recon parameters were specified. This is a requirement to run the DBRC utility.

        Raises:
            ValueError: Neither dynalloc or any recon data sets were specified.
        """
        # TODO: Determine if each of the RECONs need to be present or just 1 minimum
        if not self.dynalloc and not (self.recon1 or self.recon2 or self.recon3):
            raise ValueError("'dynalloc' or ('recon1', 'recon2', 'recon3') must be specified.")

    def _assert_valid_input_types(self):
        """This assertion function validates that all parameters are the correct data type. All
        parameters in the constructor must be strings except for 'commands' and 'steplib' which
        can also be a list of strings.

        Raises:
            TypeError: Raised if parameter is the wrong data type.
        """
        if isinstance(self.commands, str):
            self.commands = [self.commands]
        elif not isinstance(self.commands, list) and any(not isinstance(cmd, str) for cmd in self.commands):
            raise TypeError("'commands' must be a string or list of strings.")

        if isinstance(self.steplib_list, str):
            self.steplib_list = [self.steplib_list]
        elif not isinstance(self.steplib_list, list) and any(not isinstance(steplib, str) for steplib in self.steplib_list):
            raise TypeError("'steplib' must be a string or list of strings.")

        if not isinstance(self.dbdlib, str):
            raise TypeError("'dbdlib' must be a string.")

        if not isinstance(self.genjcl, str):
            raise TypeError("'genjcl' must be a string.")

        if not isinstance(self.recon1, str):
            raise TypeError("'recon1' must be a string.")
        
        if not isinstance(self.recon2, str):
            raise TypeError("'recon2' must be a string.")
        
        if not isinstance(self.recon3, str):
            raise TypeError("'recon3' must be a string.")
    
    def _extract_values(self, output_line):
        """Given a line from the output string, this function parses a line that contains
        equals signs (=), and returns a dictionary with key value pairs based on the line.

        Args:
            output_line (str): The original line of output given from the DBRC utility result.

        Returns:
            (dict): Mapping of the fields that corresponds to the line from the output
        
        Example:
            output_line: 'FORCER    LOG DSN CHECK=CHECK44    STARTNEW=NO'
            returns: {"LOG DSN CHECK": "CHECK44", "STARTNEW": False}
        """
        fields = {}
        elements = output_line.split("=")
        i = 0
        while i < len(elements) - 1:
            key_list = list(filter(None, elements[i].split("  ")))
            value_list = list(filter(None, elements[i + 1].split("  ")))

            last_key_index = len(key_list) - 1
            key = key_list[last_key_index].strip()
            if len(key_list) == 1 and i > 0 and i < len(elements) - 1:
                # print(elements, key_list)
                unformatted_key = key_list[0]
                try:
                    start_index = re.search(r'\d+\s', unformatted_key).end()
                    key = unformatted_key[start_index:].strip()
                except:
                    key = unformatted_key.strip()
            if len(value_list) == 1 and i > 0 and i < len(elements) - 1: 
                fields[key] = None
            else:
                value = value_list[0].strip()
                if value in IMSDbrc.replacement_values:
                    value = IMSDbrc.replacement_values[value]
                fields[key] = value
            i += 1
            
        return fields

    def _format_command(self, raw_command):
        """Properly formats the specific command corresponding to the output being parsed.

        Args:
            raw_command (str): Unformatted str that contains the current command.

        Returns:
            (str): Formatted command string.
        """
        if raw_command[0] == "0":
            return raw_command[1:].strip()
        return raw_command.strip()

    def _get_indentifier(self, raw_output_line):
        """Returns the "identifier" of the particular block of output being parsed.

        Args:
            raw_output_line (str): Unformatted line from the output that contains the identifier.

        Returns:
            (str): Formatted identifier extracted from the provided line of output.
        """
        return raw_output_line.split("  ")[0].strip()

    def _parse_output(self, raw_output):
        """Main function that parses the entire output provided by the zos_raw module.

        Args:
            raw_output (str): Unformatted output text provided from zos_raw module.

        Returns:
            (dict): Parsed output mappings.
            (list[str]): Original output provided by zos_raw.
        """
        original_output = [elem.strip() for elem in raw_output.split("\n")]
        output_fields = {}
        command = ''
        separation_pattern = r'-{5,}'
        rec_ctrl_pattern = r'recovery control\s*page\s\d+'
        dsp_pattern = r'DSP\d{4}I'
        output_index = 0
        for index, line in enumerate(original_output):
            if re.search(rec_ctrl_pattern, line, re.IGNORECASE) \
                and not re.search(dsp_pattern, original_output[index + 1], re.IGNORECASE):
                command = self._format_command(original_output[index + 1])
                output_fields[command] = {}
                output_fields[command]['MESSAGES'] = []
                output_fields[command]['OUTPUT'] = [{}]
                output_index = 0
            elif re.search(separation_pattern, line, re.IGNORECASE):
                if output_fields[command]['OUTPUT'][output_index]:
                    output_fields[command]['OUTPUT'].append({})
                    output_index += 1
                output_id = {"IDENTIFIER": self._get_indentifier(original_output[index + 1])}
                output_fields[command]['OUTPUT'][output_index].update(output_id)
            elif "=" in line:
                output_fields[command]['OUTPUT'][output_index].update(self._extract_values(line))
            elif re.search(dsp_pattern, line, re.IGNORECASE):
                output_fields[command]['MESSAGES'].append(line)

        return output_fields, original_output

    def _add_utility_statement(self, name, data_set, dbrc_utility_fields):
        """Adds the DD Statement to the list of dbrc_utility_fields if the data set name
        was provided.

        Args:
            name (str): Name parameter to provide to DDStatement constructor.
            data_set (str): Name of the dataset to be provided to the DatasetDefinition cosntructor.
            dbrc_utility_fields (list[str]): List that contains DDStatement objects.
        """
        if data_set:
            dbrc_utility_fields.append(DDStatement(name, DatasetDefinition(data_set)))

    def _build_utility_statements(self):
        """Builds the list DDStatements that will be provided to the zos_raw execute function
        based on the user input.

        Returns:
            (list[DDStatement]): List of DDStatements
        """
        dbrc_utility_fields = []
        steplib_data_set_definitions = [DatasetDefinition(steplib) for steplib in self.steplib_list]
        if self.dynalloc:
            steplib_data_set_definitions.append(DatasetDefinition(self.dynalloc))
        steplib = DDStatement("steplib", steplib_data_set_definitions)
        dbrc_utility_fields.append(steplib)
        self._add_utility_statement("recon1", self.recon1, dbrc_utility_fields)
        self._add_utility_statement("recon2", self.recon2, dbrc_utility_fields)
        self._add_utility_statement("recon3", self.recon3, dbrc_utility_fields)
        self._add_utility_statement("jclpds", self.genjcl, dbrc_utility_fields)
        self._add_utility_statement("ims", self.dbdlib, dbrc_utility_fields)
        dbrc_commands = StdinDefinition("\n".join(self.commands))
        sysin = DDStatement("sysin", dbrc_commands)
        sysprint = DDStatement("sysprint", StdoutDefinition())
        dbrc_utility_fields.extend([sysin, sysprint])
        return dbrc_utility_fields

    def execute(self):
        """Executes the DBRC utility dspurx00 using the zos_raw module based on the user input.

        Returns:
            (dict): (1) The original, unformatted output provided by zos_raw and (2) the parsed
                mappings for the output.
        """
        dbrc_utility_fields = self._build_utility_statements()
        response = MVSCmd.execute("dspurx00", dbrc_utility_fields)
        fields, original_output = self._parse_output(response.stdout)
        # fields, original_output = self._parse_output(TEST_INPUT)
        res = {"dbrc_fields": fields, "original_output": original_output}
        return res

