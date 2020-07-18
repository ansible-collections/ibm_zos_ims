# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

from pprint import pprint
from ibm_zos_ims.tests.functional.module_utils.ims_test_gen_utils import ACBInputParameters as ip
import pytest
__metaclass__ = type


COMMAND_INPUT_BUILD = ip.COMMAND_INPUT_BUILD
COMMAND_INPUT_DELETE = ip.COMMAND_INPUT_DELETE
PSBLIB = ip.PSBLIB
DBDLIB = ip.DBDLIB
ACBLIB = ip.ACBLIB
STEPLIB = ip.STEPLIB
RESLIB = ip.RESLIB
PSB_NAME_ALL = ip.PSB_NAME_ALL
PSB_NAME = ip.PSB_NAME
DBD_NAME = ip.DBD_NAME
DBD_NAMES = ip.DBD_NAMES
COMP_PRE = ip.COMP_PRE
COMP_POST = ip.COMP_POST
COMP = ip.COMP


def validate_acbgen(hosts, psb_name=None, dbd_name=None, psb_lib=None,
                       dbd_lib=None, acb_lib=None, steplib=None, reslib=None,
                       compression=None, build_psb=None, command_input=None):
    arguments = {}
    if psb_name:
        arguments["psb_name"] = psb_name
    if dbd_name:
        arguments["dbd_name"] = dbd_name
    if psb_lib:
        arguments["psb_lib"] = psb_lib
    if dbd_lib:
        arguments["dbd_lib"] = dbd_lib
    if acb_lib:
        arguments["acb_lib"] = acb_lib
    if steplib:
        arguments["steplib"] = steplib
    if reslib:
        arguments["reslib"] = reslib
    if compression:
        arguments["compression"] = compression
    if build_psb:
        arguments["build_psb"] = build_psb
    if command_input:
        arguments["command_input"] = command_input

    response = hosts.all.ims_acb_gen(**arguments)
    print("Result:", response)
    for result in response.contacted.values():
        pprint(result)
        print("Changed:", result.get('changed'))
        print("Return code:", result.get('rc'))
        assert result.get('changed') == True
        assert result.get('rc') <= 4


def test_ims_acb_gen_sample_build(ansible_zos_module):
    hosts = ansible_zos_module
    validate_acbgen(hosts, command_input=COMMAND_INPUT_BUILD, psb_name=PSB_NAME, psb_lib=PSBLIB, dbd_lib=DBDLIB, acb_lib=ACBLIB, steplib=STEPLIB, reslib=RESLIB)


def test_ims_acb_gen_sample_delete(ansible_zos_module):
    hosts = ansible_zos_module
    validate_acbgen(hosts, command_input=COMMAND_INPUT_DELETE, psb_name=PSB_NAME, dbd_name=DBD_NAMES, psb_lib=PSBLIB, dbd_lib=DBDLIB, acb_lib=ACBLIB, steplib=STEPLIB, reslib=RESLIB)




