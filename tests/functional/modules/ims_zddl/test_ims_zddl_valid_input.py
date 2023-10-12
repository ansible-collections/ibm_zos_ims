# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
from pprint import pprint
import pytest
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

# ------------- SQL Variables
SQL_CASELNG = "IMSTESTL.SEQ.SQLCSLNG" 
SQL_SIMPLE = "IMSTESTL.SEQ.SQLSIN" 
SQL_SPORT = "IMSTESTL.SEQ.SQLSPRT"  
SQL_DELETE = "IMSTESTL.SEQ.SQLDLT"  
SQL_EMPTY = "IMSTESTL.SEQ.SQLMPT"
SQL_INVALID = "IMSTESTL.SEQ.SQLINVLD"
SQL_MIXED = "IMSTESTL.SEQ.SQLMXVL"
SQL_NO_COMMIT = "IMSTESTL.SEQ.SQLNCM"
SQL_DTSMMBR = "IMSTESTL.PDS.SQLINP(INPMBR)"

# Control statements
VERBOSE = ip.VERBOSE
AUTO_COMMIT = ip.AUTO_COMMIT
SIMULATE = ip.SIMULATE
dynamic_programview = ip.dynamic_programview

"""
Work flow for Combination functional tests goes as follows:
------------------------------------ Running on BMP ------------------------------------
1. Delete the databases created during the execution of the test cases
2. Send only proclib and sql_input ONLINE IMS ID
3. IMS ID with ONLINE with all variables 
4. Multi line Sql Input
5. Multi line Sql Input over 6 instructions
6. Verbose with auto-commit
7. No control statements
8. Simulation, auto-commit and verbose
9. Dynamic Program view with simulation and auto-commit
10. Input as a dataset member
11. Only dynamic program view
------------------------------------ Not supporting DLI, so these are commented ------------------------------------
12. IRLM Specified
13. Offline simulation
"""

def validate_zddl(hosts, online:bool=None, ims_id:str=None,
                            irlm_id:str=None, reslib:list=None, proclib:list=None,
                            steplib:list=None, sql_input:list=None, verbose:bool=None,
                            auto_commit:bool=None, simulate:bool=None, dynamic_programview:bool=None
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
    if dynamic_programview:
        arguments["dynamic_programview"] = dynamic_programview
    response = hosts.all.ims_ddl(**arguments)
    print("Result:", response)
    for result in response.contacted.values():
        pprint(result)
        print("Return code:", result.get('rc'))

        assert result.get('rc') <= 4

# 1. Delete the databases created during the execution of the test cases
def test_ims_zddl_delete_sql_dataset(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=IRLM_ID, reslib=None, proclib=PROCLIB,
                            steplib=None, sql_input=SQL_DELETE, verbose=False,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, dynamic_programview=False)

# 2. Send only proclib and sql_input: This is because these are the only two required parameters, it should work without the others(except for IMS_ID when ONLINE)
def test_ims_zddl_valid_only_proclib_sql_input(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=None, proclib=PROCLIB,
                            steplib=None, sql_input=SQL_SIMPLE, verbose=None,
                            auto_commit=None, simulate=None, dynamic_programview=None)

# 3. IMS ID with ONLINE: Chechs that when given ONLINE and IMS_ID it works
def test_ims_zddl_valid_ims_id_online(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=None, proclib=PROCLIB,
                            steplib=None, sql_input=SQL_SIMPLE, verbose=None,
                            auto_commit=None, simulate=None, dynamic_programview=None)
    
# 4. Multi line Sql Inputs: Test the sports sql commands(Recieved from core DDL team)
def test_ims_zddl_valid_multi_sql(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=None, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_SPORT, verbose=None,
                            auto_commit=None, simulate=None, dynamic_programview=None)
    
# 5. Extensive sql dataset: Test the sql commands on W1D150P(Recieved from core DDL team)
def test_ims_zddl_valid_over_six_sql(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=None, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_CASELNG, verbose=VERBOSE,
                            auto_commit=None, simulate=None, dynamic_programview=None)

# 6. Online verbose with auto-commit: Control statements variation for online and verbose
def test_ims_zddl_valid_online_verbose_auto_commit(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=None, proclib=PROCLIB,
                            steplib=None, sql_input=SQL_SIMPLE, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=None, dynamic_programview=False)

# 7. All control statements at once: Test that you can put all the four statemnts as True at once
def test_ims_zddl_valid_all_control_statements(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=IRLM_ID, reslib=None, proclib=PROCLIB,
                            steplib=None, sql_input=SQL_SIMPLE, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, dynamic_programview=dynamic_programview)

# 8. Simulation and auto-commit: Variation of the control statements variables
def test_ims_zddl_valid_control_statements_no_verbose(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=IRLM_ID, reslib=None, proclib=PROCLIB,
                            steplib=None, sql_input=SQL_SIMPLE, verbose=False,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, dynamic_programview=False)

# 9. Dynamic Program view with simulation and auto-commit: Variation of the control statements variables
def test_ims_zddl_valid_control_statements_program_view(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=IRLM_ID, reslib=None, proclib=PROCLIB,
                            steplib=None, sql_input=SQL_SIMPLE, verbose=False,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, dynamic_programview=True)    
    
# 10. Input as a dataset member: 
def test_ims_zddl_valid_dataset_member(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=IRLM_ID, reslib=None, proclib=PROCLIB,
                            steplib=None, sql_input=SQL_DTSMMBR, verbose=False,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, dynamic_programview=True)   

# 11. Only dynamic program view
def test_ims_zddl_valid_only_dynamic_programview(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=IRLM_ID, reslib=None, proclib=PROCLIB,
                            steplib=None, sql_input=SQL_SIMPLE, verbose=False,
                            auto_commit=False, simulate=False, dynamic_programview=True) 

# 12. IRLM Specified: Checks that when OFFLINE, works when IRLM_ID is provided (DLI test case)
# def test_ims_zddl_valid_irlm(ansible_zos_module):
#     hosts = ansible_zos_module
#     validate_zddl(hosts, online=False, ims_id=None,
#                             irlm_id=IRLM_ID, reslib=None, proclib=PROCLIB,
#                             steplib=None, sql_input=SQL_SIMPLE, verbose=None,
#                             auto_commit=None, simulate=None, dynamic_programview=None)
    
# 13. Offline simulation (DLI test case): Variation of control statements variable for an OFFLINE scenario
# def test_ims_zddl_valid_offline_simulation(ansible_zos_module):
#     hosts = ansible_zos_module
#     validate_zddl(hosts, online=OFFLINE, ims_id=None,
#                             irlm_id=IRLM_ID, reslib=None, proclib=PROCLIB,
#                             steplib=None, sql_input=SQL_SPORT, verbose=None,
#                             auto_commit=None, simulate=SIMULATE, dynamic_programview=None)

