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


def test_ims_acb_gen_sample_build(ansible_zos_module):
    hosts = ansible_zos_module

    results = hosts.all.ims_acb_gen(
        command_input=COMMAND_INPUT_BUILD,
        psb_name=PSB_NAME,
        psb_lib=PSBLIB,
        dbd_lib=DBDLIB,
        acb_lib=ACBLIB,
        reslib=RESLIB,
        steplib=STEPLIB,
    )
    print("Result:", results)
    for result in results.contacted.values():
        pprint(result)
        print("Changed:", result['changed'])
        assert result['changed'] == True
        assert result['rc'] <= '4'


def test_ims_acb_gen_sample_delete(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_acb_gen(
        command_input=COMMAND_INPUT_DELETE,
        psb_name=PSB_NAME,
        dbd_name=DBD_NAMES,
        psb_lib=PSBLIB,
        dbd_lib=DBDLIB,
        acb_lib=ACBLIB,
        reslib=RESLIB,
        steplib=STEPLIB,
    )
    print("Result:", results)
    for result in results.contacted.values():
        pprint(result)
        print("Changed:", result['changed'])
        assert result['changed'] == True
        assert result['rc'] <= '4'




