# Copyright (c) IBM Corporation 2019, 2020
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# Important constants
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError, AnsibleFileNotFound
from tempfile import NamedTemporaryFile
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import (
    BetterArgParser,
)
import os
import time
import re


def build_dd(ddname, ddlist):
    singleddstr = "DD DSN={0}," +"\n//   " + "DISP=SHR"
    ddstring = "//{0}  {1}\n".format(ddname, singleddstr.format(ddlist[0]))
    for dd in ddlist[1:]:
        ddstring += "//   {0}\n".format("  " + singleddstr.format(dd))
    return ddstring


def build_dd_steplib(ddname, ddlist, steplib):
    singleddstr = "DD DSN={0}," +"\n//   " + "DISP=SHR"
    if ddlist:
        ddstring = "//{0}  {1}\n".format(ddname, singleddstr.format(ddlist[0]))
        for dd in ddlist[1:]:
            ddstring += "//   {0}\n".format("  " + singleddstr.format(dd))
    else:
        ddstring = "//{0}  {1}\n".format(ddname, singleddstr.format(steplib))
    return ddstring


def build_psb_name_string(command_input, psbnames):
    psb_str = ""
    if psbnames:
        for psb in psbnames:
            #if a match is not found
            if not re.fullmatch(r'[A-Z$#@]{1}[A-Z0-9$#@]{0,7}', psb, re.IGNORECASE):
                return False, psb
            else: 
                # if a match is found
                if psb == "ALL":
                    psb_str = command_input + " PSB=ALL"
                    break
                else:    
                    psb_str = command_input + " PSB=(" + ",".join(psbnames) + ")"
    return True, psb_str    


def split_lines_dbd(command_input, dbdnames, bldpsb):
    return_arr = []
    return_bool = False
    if len(dbdnames) < 6:
        return_bool, return_str = build_dbd_name_string(command_input, dbdnames, bldpsb)
        return return_bool, return_str
    else:
        for i in range(0, len(dbdnames), 5):
            new_db_names_five = dbdnames[i: i + 5]
            return_bool, dbd_line = build_dbd_name_string(command_input, new_db_names_five, bldpsb)
            return_arr.append(dbd_line)
        return return_bool, "\n ".join(return_arr)
    return return_bool, return_arr    
      

def split_lines_psb(command_input, psbnames):
    return_arr = []
    return_bool = False
    if len(psbnames) < 6:
        return_bool, return_str = build_psb_name_string(command_input, psbnames)
        return return_bool, return_str
    else:
        for i in range(0, len(psbnames), 5):
            new_db_names_five = psbnames[i: i + 5]
            return_bool, psb_line = build_psb_name_string(command_input, new_db_names_five)
            return_arr.append(psb_line)
        return return_bool, "\n ".join(return_arr)
    return return_bool, return_arr          
    

def build_dbd_name_string(command_input, dbdnames, bldpsb):
    dbd_str = ""
    bldpsb_value = ""
    if bldpsb:
        bldpsb_value = "YES"
    else:
        bldpsb_value = "NO"

    if dbdnames:
        for dbd in dbdnames:
            #if a match is not found
            if not re.fullmatch(r'[A-Z$#@]{1}[A-Z0-9$#@]{0,7}', dbd, re.IGNORECASE):
                return False, dbd
            else:
                # if a match is found
                if dbdnames and bldpsb:
                    dbd_str = command_input + " DBD=(" + ",".join(dbdnames) + ")"
                elif dbdnames and command_input == "BUILD":
                    dbd_str = (
                        command_input
                        + " DBD=("
                        + ",".join(dbdnames)
                        + ")"
                        + ",BLDPSB="
                        + bldpsb_value
                    )
                elif dbdnames:
                    dbd_str = command_input + " DBD=(" + ",".join(dbdnames) + ")"
    return True, dbd_str


def str_or_list_of_str(contents, dependencies):
    if isinstance(contents, list):
        for item in contents:
            if not isinstance(item, str):
                raise ValueError(
                    "Items provided in list do not match the string type expected."
                )
    elif isinstance(contents, str):
        contents = [contents]  # make this a list of strings to consistent format
    else:
        raise ValueError(
            "Incorrect type provided. A string or list of strings is expected"
        )
    return contents


ZOAU_TEMP_USS = "/tmp/test.jcl"


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        """handler for file transfer operations."""
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        if result.get("skipped"):
            return result

        module_args = self._task.args.copy()

        # Retrieve properties set by the user
        module_defs = dict(
            command_input=dict(arg_type="str", required=True),
            comp=dict(arg_type="str", required=False, default=""),
            psb_name=dict(arg_type=str_or_list_of_str, required=False),
            dbd_name=dict(arg_type=str_or_list_of_str, elements="str", required=False),
            acb_lib=dict(arg_type="str", required=True),
            psb_lib=dict(arg_type="list", elements="str", required=True),
            dbd_lib=dict(arg_type="list", elements="str", required=True),
            res_lib=dict(arg_type="list", elements="str", required=False),
            steplib=dict(arg_type="list", elements="str", required=False),
            bld_psb=dict(arg_type="bool", required=False, default=True),
        )

        # Parse the properties
        parser = BetterArgParser(module_defs)
        parsed_args = parser.parse_args(module_args)

        command_input = parsed_args.get("command_input")
        comp = parsed_args.get("comp")
        psb_name = parsed_args.get("psb_name")
        dbd_name = parsed_args.get("dbd_name")
        acb_lib = parsed_args.get("acb_lib")
        psb_lib = parsed_args.get("psb_lib")
        dbd_lib = parsed_args.get("dbd_lib")
        res_lib = parsed_args.get("res_lib")
        steplib = parsed_args.get("steplib")
        bld_psb = parsed_args.get("bld_psb")

        psb_name_str = ""
        if psb_name:
            psb_name_str, psb = split_lines_psb(command_input, psb_name)
            if psb_name_str:
                if psb:
                    psb_name_str = '\n ' + psb
                else:
                    psb_name_str = psb    
            elif psb:
                msg = 'A PSB named ' + str(psb) + ' provided in the module input was not found.'
                result['rc'] = -1
                result['msg'] = msg 
                return result  
        
        dbd_name_str = ""
        if dbd_name:
            dbd_name_str, dbd = split_lines_dbd(command_input, dbd_name, bld_psb)
            print("dbd-name:", dbd_name)
            if dbd_name_str:
                dbd_name_str = '\n ' + dbd 
            else:
                msg = 'A DBD named ' + str(dbd) + ' provided in the module input was not found.'
                result['rc'] = -1
                result['msg'] = msg 
                return result 
        
        job_card = task_vars["JOB_CARD"]
        env_steplib = task_vars["environment_vars"]["STEPLIB"]
        dd_steplib = build_dd_steplib("STEPLIB", steplib, env_steplib)

        dd_reslib = ""
        if res_lib:
            dd_reslib = build_dd("DFSRESLB", res_lib)
        # Create string for the JCL contents and fill in the values
        acbgen_jcl = """{8}
//*
//ACBGEN PROC SOUT=A,COMP='{0}'
//G      EXEC PGM=DFSRRC00,PARM='UPB,&COMP'
//SYSPRINT DD SYSOUT=&SOUT
{1}{2}{3}{4}//IMSACB   DD DSN={5},DISP=OLD
//COMPCTL  DD *
   COPY  INDD=IMSACB,OUTDD=IMSACB
// PEND
//*
//STEPA EXEC ACBGEN
//SYSIN    DD *{6}{7}
/*
""".format(
            comp,
            dd_steplib,
            dd_reslib,
            build_dd("IMS", psb_lib),
            build_dd("", dbd_lib),
            acb_lib,
            psb_name_str,
            dbd_name_str,
            job_card,
        )

        # Get a temporary file on the controller and write to a it
        # Initialize JCL temp file
        delete_on_close = True
        tmp_file = NamedTemporaryFile(delete=delete_on_close)
        with open(tmp_file.name, "w") as f:
            f.write(acbgen_jcl)
        for line in tmp_file:
            print(line)

        result = {}
        module_args = self._task.args.copy()

        # Define file paths of the local controller file and the remote destination file
        dest = ZOAU_TEMP_USS
        source = tmp_file.name

        # Make sure the source file is able to be found
        try:
            source = self._find_needle("files", source)
            print(source)
        except AnsibleError as e:
            result["failed"] = True
            result["msg"] = to_text(e)
            return result

        if tmp is None or "-tmp-" not in tmp:
            tmp = self._make_tmp_path()

        # Locate the actual location of the file in the Ansible controller
        try:
            source_full = self._loader.get_real_file(source)
            source_rel = os.path.basename(source)
        except AnsibleFileNotFound as e:
            result["failed"] = True
            result["msg"] = "could not find src=%s, %s" % (source_full, e)
            self._remove_tmp_path(tmp)
            return result

        if self._connection._shell.path_has_trailing_slash(dest):
            dest_file = self._connection._shell.join_path(dest, source_rel)
        else:
            dest_file = self._connection._shell.join_path(dest)

        dest_status = self._execute_remote_stat(
            dest_file, all_vars=task_vars, follow=False
        )

        if dest_status["exists"] and dest_status["isdir"]:
            self._remove_tmp_path(tmp)
            result["failed"] = True
            result["msg"] = "can not use content with a dir as dest"
            return result

        tmp_src = self._connection._shell.join_path(tmp, "source")

        remote_path = None
        remote_path = self._transfer_file(source_full, tmp_src)

        if remote_path:
            self._fixup_perms2((tmp, remote_path))

        # Generate arguments to call the copy module
        copy_args = dict(
            src=tmp_src, dest=dest, mode="0755", _original_basename=source_rel,
        )

        # Run the copy module to copy JCL temp file with proper input values from user to z/OS USS
        result.update(
            self._execute_module(
                module_name="copy", module_args=copy_args, task_vars=task_vars,
            )
        )
        # After successfully copying the module to the remote host, return to the ims_acb_gen to submit the JCL
        result.update(
            self._execute_module(
                module_name="ims_acb_gen", module_args=module_args, task_vars=task_vars,
            )
        )

        time.sleep(5)

        jobId = result["jobId"]

        # Generate arguments to call the zos_job_output module
        job_query_args = dict(job_id=jobId)

        # Run the zos_job_output module to get the results of the jcl being submitted
        result.update(
            self._execute_module(
                module_name="zos_job_output",
                module_args=job_query_args,
                task_vars=task_vars,
            )
        )

        return_code = ""
        job_content = ""
        ddnames = ""
        module_changed = False

        listJobs = result["jobs"]
        for i in listJobs:
            for k in i.keys():
                if k == "ret_code":
                    return_code = i.get("ret_code")
                if k == "ddnames":
                    ddnames = i.get("ddnames")
                    for x in ddnames:
                        for y in x.keys():
                            if y == "content":
                                job_content = x.get("content")

        if return_code["msg_code"] == "0000" or return_code["msg_code"] == "0004":
            module_changed = True
            rc = "0"
            return_code["msg_txt"] = 'ACBGEN execution is successful'
        else:
            rc = return_code["msg_code"]
            return_code["msg_txt"] = 'ACBGEN execution unsuccessful.'

        newResult = dict(
            content=job_content, changed=module_changed, rc=rc, msg=return_code["msg_txt"]
        )

        return newResult
