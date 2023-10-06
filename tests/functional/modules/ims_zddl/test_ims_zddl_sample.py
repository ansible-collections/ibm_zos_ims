# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
import pytest
from pprint import pprint
from ibm_zos_ims.tests.functional.module_utils.ims_test_zddl_utils import ZDDLInputParameters as ip
__metaclass__ = type

# ------------- VARIABLES
ONLINE = ip.ONLINE 
OFFLINE = ip.OFFLINE
IMS_ID = ip.IMS_ID
IRLM_ID = ip.IRLM_ID 
RESLIB = ip.RESLIB 
PROCLIB = ip.PROCLIB 
STEPLIB = ip.STEPLIB
SQL_INPUT = "IMSTESTL.SEQ.SQLSIN"

# Control statements
VERBOSE = ip.VERBOSE
AUTO_COMMIT = ip.AUTO_COMMIT
SIMULATE = ip.SIMULATE
CREATE_PROGRAM_VIEW = ip.CREATE_PROGRAM_VIEW

def validate_zddl(hosts, online:bool=None, ims_id:str=None,
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

def test_ims_zddl(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_INPUT, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)
