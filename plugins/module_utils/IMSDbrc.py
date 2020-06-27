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
        self._assert_valid_input_types()
        self._assert_dynalloc_recon_requirement()

    def _assert_dynalloc_recon_requirement(self):
        # TODO: Determine if each of the RECONs need to be present or just 1 minimum
        if not self.dynalloc and not (self.recon1 or self.recon2 or self.recon3):
            raise ValueError("'dynalloc' or ('recon1', 'recon2', 'recon3') must be specified.")

    def _assert_valid_input_types(self):
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
        
    
    def _extract_values(self, elements):
        fields = {}
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
        if raw_command[0] == "0":
            return raw_command[1:].strip()
        return raw_command.strip()

    def _get_indentifier(self, raw_output_line):
        return raw_output_line.split("  ")[0].strip()

    def _parse_output(self, raw_output):
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
                elements = line.split("=")
                output_fields[command]['OUTPUT'][output_index].update(self._extract_values(elements))
            elif re.search(dsp_pattern, line, re.IGNORECASE):
                output_fields[command]['MESSAGES'].append(line)

        return output_fields, original_output

    def _build_command(self):
        dbrc_utility_fields = []
        steplib_datasets = [DatasetDefinition(steplib) for steplib in self.steplib_list]
        steplib = DDStatement("steplib", steplib_datasets)
        recon1 = DDStatement("recon1", DatasetDefinition(self.recon1))
        recon2 = DDStatement("recon2", DatasetDefinition(self.recon2))
        recon3 = DDStatement("recon3", DatasetDefinition(self.recon3))
        jclpds = DDStatement("jclpds", DatasetDefinition(self.genjcl))
        ims = DDStatement("ims", DatasetDefinition(self.dbdlib))
        dbrc_commands = [StdinDefinition("\n".join(self.commands))]
        sysin = DDStatement("sysin", dbrc_commands)
        sysprint = DDStatement("sysprint", StdoutDefinition())

        dbrc_utility_fields = [steplib, recon1, recon2, recon3, jclpds, ims, sysin, sysprint]
        return dbrc_utility_fields

    def execute(self):
        dbrc_utility_fields = self._build_command()
        response = MVSCmd.execute("dspurx00", dbrc_utility_fields)
        fields, original_output = self._parse_output(response.stdout)
        # fields, original_output = self._parse_output(TEST_INPUT)
        res = {"dbrc_fields": fields, "original_output": original_output}
        return res

