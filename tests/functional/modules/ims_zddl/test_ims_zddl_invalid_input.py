# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
from pprint import pprint
import pytest
from ibm_zos_ims.tests.functional.module_utils.ims_test_zddl_utils import ZDDLInputParameters as ip

__metaclass__ = type

"""
Work flow for Combination functional tests goes as follows:
------------------------------------ Running on BMP ------------------------------------
1. Invalid IMS ID                                   Online
2. Invalid IRLM ID                                  Online
3. Invalid RESLIB -                                 Online
4. Invalid PROCLIB -                                Online
5. Invalid STEPLIB -                                Online
6. Invalid SQL Input                                Online
7. Empty SQL Input(EMPTY LIST)                      Online
8. Valid and invalid SQL Input 
9. No proclib
10. No Sql_Input (SQL INPUT AS NONE)
11. No commit
12. Program view with no database
------------------------------------ Not supporting DLI, so these are commented ------------------------------------
13. Invalid RESLIB                                  Offline
14. Invalid PROCLIB                                 Offline
15. Invalid STEPLIB                                 Offline
16. Empty STEPLIB                                   Offline
17. Invalid SQL Input                               Offline
18. Empty SQL Input                                 Offline
19. Valid IMS ID but offline
"""

# ------------- VARIABLES
# "DEFAULT" VALUES
ONLINE = ip.ONLINE 
OFFLINE = ip.OFFLINE            
IMS_ID = ip.IMS_ID              
IRLM_ID = ip.IRLM_ID          
RESLIB = ip.RESLIB           
PROCLIB = ip.PROCLIB 
STEPLIB = ip.STEPLIB

# ------------- SQL Variables
SQL_FUll1 = "IMSTESTL.SEQ.SQLFRS1" 
SQL_SIMPLE = "IMSTESTL.SEQ.SQLSIN" 
SQL_SPORT = "IMSTESTL.SEQ.SQLSPRT"  
SQL_DELETE = "IMSTESTL.SEQ.SQLDLT"  
SQL_EMPTY = "IMSTESTL.SEQ.SQLMPT"
SQL_INVALID = "IMSTESTL.SEQ.SQLINVLD"
SQL_MIXED = "IMSTESTL.SEQ.SQLMXVL"
SQL_NO_COMMIT = "IMSTESTL.SEQ.SQLNCM" 
SQL_NO_DB_PRGVIEW = "IMSTESTL.SEQ.SQLNCS" 

# Control statements
VERBOSE = ip.VERBOSE
AUTO_COMMIT = ip.AUTO_COMMIT
SIMULATE = ip.SIMULATE
CREATE_PROGRAM_VIEW = ip.CREATE_PROGRAM_VIEW

# INVALID VALUES
INVALID_IMS_ID = ip.INVALID_IMS_ID
INVALID_IRLM_ID = ip.INVALID_IRLM_ID
INVALID_STEPLIB = ip.INVALID_STEPLIB
INVALID_RESLIB = ip.INVALID_RESLIB
INVALID_PROCLIB = ip.INVALID_PROCLIB
INVALID_SQL_INPUT = ip.INVALID_SQL_INPUT
EMPTY_SQL_INPUT = ip.EMPTY_SQL_INPUT
MIXED_SQL_INPUT = ip.MIXED_SQL_INPUT
# -------------

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
        print(result.get('msg'))
        if result.get('rc'):
            assert result.get('rc') != 0

# 1. Invalid IMS ID: Validate that an invalid value for IMS_ID won't be accepted
def test_ims_zddl_invalid_ims_id(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=INVALID_IMS_ID,
                            irlm_id=None, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_SIMPLE, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# 2. Invalid IRLM ID: When OFFLINE, verify that the IRLM_ID won't be accepted if the value is inconrrect
def test_ims_zddl_invalid_irlm_id(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=OFFLINE, ims_id=None,
                            irlm_id=INVALID_IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_SIMPLE, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# 3. Invalid RESLIB: Validate that an existent/valid reslib is needed when specified
def test_ims_zddl_invalid_reslib(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=INVALID_RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_SIMPLE, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)


# 4. Invalid PROCLIB: Validate that an existent/valid proclib is needed when specified
def test_ims_zddl_invalid_proclib(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=RESLIB, proclib=INVALID_PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_SIMPLE, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)


# 5. Invalid STEPLIB: Validate that an existent/valid steplib is needed when specified
def test_ims_zddl_invalid_steplib(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=RESLIB, proclib=PROCLIB,
                            steplib=INVALID_STEPLIB, sql_input=SQL_SIMPLE, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# 6. Invalid SQL Input: SQL_input needs to use sql commands as arguments, this test case check the user only provides this kind of arguments
def test_ims_zddl_invalid_sql(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_INVALID, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# 7. Empty SQL Input: SQL_input is required, so here we make sure that the given value cannot be an empty list
def test_ims_zddl_empty_sql(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_EMPTY, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# 8. Valid and invalid SQL Input: This make sure that the reading of one valid sql command doesn't cause that the whole list be valid
def test_ims_zddl_valid_invalid_sql(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_MIXED, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# 9. No Proclib: Proclib is required, so here we check that it cannot be None when running ddl
def test_ims_zddl_invalid_no_given_proclib(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=RESLIB, proclib=None,
                            steplib=STEPLIB, sql_input=SQL_SIMPLE, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# 10. No Sql_Input: SQL_input is required, so here we check that it cannot be None when running ddl
def test_ims_zddl_invalid_no_given_sql(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=None, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# 11. No commit: SQL dataset need the commit ddl command, so here we check that if is not in the dataset, it fails
def test_ims_zddl_no_commit(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_NO_COMMIT, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# 12. Program view with no database: This test case try to create a program view on an unexistent database 
def test_ims_zddl_invalid_prgview_no_database(ansible_zos_module):
    hosts = ansible_zos_module
    validate_zddl(hosts, online=ONLINE, ims_id=IMS_ID,
                            irlm_id=None, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, sql_input=SQL_NO_DB_PRGVIEW, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# # 13. Invalid RESLIB - LIB authorized and exists - Offline
# def test_ims_zddl_invalid_reslib(ansible_zos_module):
#     hosts = ansible_zos_module
#     validate_zddl(hosts, online=OFFLINE, ims_id=None,
#                             irlm_id=IRLM_ID, reslib=INVALID_RESLIB, proclib=PROCLIB,
#                             steplib=STEPLIB, sql_input=SQL_INPUT, verbose=VERBOSE,
#                             auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)


# # 14. Invalid PROCLIB - LIB authorized and exists - Offline
# def test_ims_zddl_invalid_proclib(ansible_zos_module):
#     hosts = ansible_zos_module
#     validate_zddl(hosts, online=OFFLINE, ims_id=None,
#                             irlm_id=IRLM_ID, reslib=RESLIB, proclib=INVALID_PROCLIB,
#                             steplib=STEPLIB, sql_input=SQL_INPUT, verbose=VERBOSE,
#                             auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)


# # 15. Invalid STEPLIB - LIB authorized and exists - Offline
# def test_ims_zddl_invalid_steplib(ansible_zos_module):
#     hosts = ansible_zos_module
#     validate_zddl(hosts, online=OFFLINE, ims_id=None,
#                             irlm_id=IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
#                             steplib=INVALID_STEPLIB, sql_input=SQL_INPUT, verbose=VERBOSE,
#                             auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)


# # 16. Empty STEPLIB - LIB dont exists - Offline
# def test_ims_zddl_empty_steplib(ansible_zos_module):
#     hosts = ansible_zos_module
#     validate_zddl(hosts, online=OFFLINE, ims_id=None,
#                             irlm_id=IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
#                             steplib=EMPTY_STEPLIB, sql_input=SQL_INPUT, verbose=VERBOSE,
#                             auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)


# # 17. Invalid SQL Input - Offline
# def test_ims_zddl_invalid_sql(ansible_zos_module):
#     hosts = ansible_zos_module
#     validate_zddl(hosts, online=OFFLINE, ims_id=None,
#                             irlm_id=IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
#                             steplib=STEPLIB, sql_input=INVALID_SQL_INPUT, verbose=VERBOSE,
#                             auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# # 18. Empty SQL Input - Offline
# def test_ims_zddl_invalid_sql(ansible_zos_module):
#     hosts = ansible_zos_module
#     validate_zddl(hosts, online=OFFLINE, ims_id=None,
#                             irlm_id=IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
#                             steplib=STEPLIB, sql_input=EMPTY_SQL_INPUT, verbose=VERBOSE,
#                             auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)

# 19. Valid IMS ID but offline
# def test_ims_zddl_invalid_sql(ansible_zos_module):
#     hosts = ansible_zos_module
#     validate_zddl(hosts, online=OFFLINE, ims_id=IMS_ID,
#                             irlm_id=IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
#                             steplib=STEPLIB, sql_input=SQL_INPUT, verbose=VERBOSE,
#                             auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)