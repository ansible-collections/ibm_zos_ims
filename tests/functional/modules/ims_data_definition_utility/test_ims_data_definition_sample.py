# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from pprint import pprint
from ibm_zos_ims.tests.functional.module_utils.ims_test_data_definition_utils import ZDDLInputParameters as ip
from ibm_zos_ims.tests.functional.module_utils.ims_test_gen_utils import DBDInputParameters as dbd
from ibm_zos_ims.tests.functional.module_utils.ims_test_gen_utils import PSBInputParameters as psb

import pytest
__metaclass__ = type


ONLINE_BATCH_TRUE = ip.ONLINE_BATCH_TRUE # In the documentation it appears as online, but in the examples it's written as online_batch
ONLINE_BATCH_FALSE = ip.ONLINE_BATCH_FALSE # In the documentation it appears as online, but in the examples it's written as online_batch
IMS_ID = ip.ID
IRLM_ID = ip.IRLM_ID # I made up the value for this variable
RESLIB = ip.RESLIB
PROCLIB = ip.PROCLIB # The content in the test utils file must have a list with possible values for this variable, for now, I'll just put "PROCLIB"
STEPLIB = ip.STEPLIB
IMS_SQL = ip.IMS_SQL # In the documentation appears as SQL_input, but in the examples it's declared as ims_sql
VERBOSE = ip.VERBOSE
AUTO_COMMIT = ip.AUTO_COMMIT
SIMULATE = ip.SIMULATE
CREATE_PROGRAM_VIEW = ip.CREATE_PROGRAM_VIEW

# vars for prereqs
COMMAND_INPUT_BUILD = ip.COMMAND_INPUT_BUILD
ACBLIB = ip.ACBLIB
PSBLIB = ip.PSBLIB
DBDLIB = ip.DBDLIB
DBD_NAME = ip.DBD_NAME
DBD_NAMES = ip.DBD_NAMES


def validate_data_definition(hosts, online_batch=None, ims_id=None,
                            irlm_id=None, reslib=None, proclib=None,
                            steplib=None, ims_sql=None, verbose=None,
                            auto_commit=None, simulate=None, create_program_view=None):
    arguments = {}
    if online_batch:
        arguments["online_batch"] = online_batch
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
    if ims_sql:
        arguments["ims_sql"] = ims_sql
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
        #print("Changed:", result.get('changed')) # No change variable
        print("Return code:", result.get('rc'))
        #assert result.get('changed')
        assert result.get('rc') <= 4


def test_managed_acb_prereq(ansible_zos_module):
    hosts = ansible_zos_module
    response = hosts.all.ims_acb_gen(
         # set the instructions for the ACB GEN validation
        command_input=COMMAND_INPUT_BUILD, 
        aclib=ACBLIB, 
        psb_lib=PSBLIB,
        dbd_lib=DBDLIB, 
    )
    for result in response.contacted.values():
        print(result)
        print("Changed:", result['changed'])
        assert result['changed']
        assert result['rc'] == 0


def test_ims_data_definition_online(ansible_zos_module):
    hosts = ansible_zos_module
    validate_data_definition(hosts, online_batch=ONLINE_BATCH_TRUE, ims_id=IMS_ID,
                            irlm_id=IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, ims_sql=IMS_SQL, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)


def test_ims_data_definition_offline(ansible_zos_module):
    hosts = ansible_zos_module
    validate_data_definition(hosts, online_batch=ONLINE_BATCH_FALSE, ims_id=IMS_ID,
                            irlm_id=IRLM_ID, reslib=RESLIB, proclib=PROCLIB,
                            steplib=STEPLIB, ims_sql=IMS_SQL, verbose=VERBOSE,
                            auto_commit=AUTO_COMMIT, simulate=SIMULATE, create_program_view=CREATE_PROGRAM_VIEW)