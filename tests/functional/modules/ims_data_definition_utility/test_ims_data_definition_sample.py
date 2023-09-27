# -*- coding: utf-8 -*-
# ./run.sh test_config.yml functional/modules/ims_data_definition_utility/test_ims_data_definition_sample.py
from __future__ import (absolute_import, division, print_function)
import pytest
from pprint import pprint
from ibm_zos_ims.tests.functional.module_utils.ims_test_data_definition_utils import ZDDLInputParameters as ip
__metaclass__ = type

# ------------- VARIABLES
ONLINE = ip.ONLINE 
OFFLINE = ip.OFFLINE
IMS_ID = ip.IMS_ID
IRLM_ID = ip.IRLM_ID # I made up the value for this variable
RESLIB = ip.RESLIB  # The next 4 variables are lists
PROCLIB = ip.PROCLIB 
STEPLIB = ip.STEPLIB
SQL_INPUT = "IMSTESTL.SEQ.SQLFUL"  # SQLSIN, SQLMID, SQLFUL, SQLMPT

# Control statements
VERBOSE = ip.VERBOSE
AUTO_COMMIT = ip.AUTO_COMMIT
SIMULATE = ip.SIMULATE
CREATE_PROGRAM_VIEW = ip.CREATE_PROGRAM_VIEW

# vars for prereqs
# COMMAND_INPUT_BUILD = ip.COMMAND_INPUT_BUILD
# ACBLIB = ip.ACBLIB
# PSBLIB = ip.PSBLIB
# DBDLIB = ip.DBDLIB
# DBD_NAME = ip.DBD_NAME
# DBD_NAMES = ip.DBD_NAMES
# -------------


def validate_data_definition(hosts, online:bool=None, ims_id:str=None,
                            irlm_id:str=None, reslib:list=None, proclib:list=None,
                            steplib:list=None, sql_input:list=None, verbose:bool=None,
                            auto_commit:bool=None, simulate:bool=None, create_program_view:bool=None
                            ):
    arguments = {}
    if online:
        arguments["online"] = online
    if ims_id:
        arguments["ims_id"] = ims_id
    if irlm_id:
        arguments["irlm_id"] = irlm_id
    if reslib:
        arguments["reslib"] = reslib
    if proclib:
        arguments["proclib"] = proclib
    if steplib:
        arguments["steplib"] = steplib
    if sql_input:
        arguments["sql_input"] = sql_input
    if verbose:
        arguments["verbose"] = verbose
    if auto_commit:
        arguments["auto_commit"] = auto_commit
    if simulate:
        arguments["simulate"] = simulate
    if create_program_view:
        arguments["create_program_view"] = create_program_view
    response = hosts.all.ims_ddl(**arguments)
    print("Result:", response)
    for result in response.contacted.values():
        pprint(result)
        print("Changed:", result.get('changed')) # No change variable
        print("Return code:", result.get('rc'))
        #assert result.get('changed')
        assert result.get('rc') == 0


# # set the instructions for the ACB GEN validation
# def test_managed_acb_prereq(ansible_zos_module):
#     hosts = ansible_zos_module
#     response = hosts.all.ims_acb_gen(
#         command_input=COMMAND_INPUT_BUILD, 
#         aclib=ACBLIB, 
#         psb_lib=PSBLIB,
#         dbd_lib=DBDLIB, 
#     )
#     for result in response.contacted.values():
#         print(result)
#         print("Changed:", result['changed'])
#         assert result['changed']
#         assert result['rc'] == 0


def test_ims_data_definition(ansible_zos_module):
    hosts = ansible_zos_module
    validate_data_definition(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_INPUT, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)



# def test_ims_data_definition_offline(ansible_zos_module): # Delete this ????????????
#     hosts = ansible_zos_module
#     validate_data_definition(hosts, online=OFFLINE, ims_id=IMS_ID,
#                             irlm_id=IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
#                             steplib=STEPLIB, sql_input=SQL_INPUT, verbose=VERBOSE,
#                             auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)
