# -*- coding: utf-8 -*-

from pprint import pprint
import pytest
from ibm_zos_ims.tests.functional.module_utils.ims_test_gen_utils import ACBInputParameters as ip


__metaclass__ = type

JOB_CARD = ip.JOB_CARD
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


"""
Work flow for Combination functional tests goes as follows:
1. BUILD PSB=ALL as string
2. DELETE PSB=PSB_NAME as list 
3. BUILD PSB=PSB_NAME
4. DELETE DBD=DBD_NAME
5. BUILD DBD=DBD_NAME,BLDPSB=NO
6. BUILD DBD=DBD_NAME,BLDPSB=YES 
7. BUILD PSB=PSB_NAME
8. DELETE PSB=PSB_NAME, DELETE DBD=DBD_NAMES
9. BUILD PSB=PSB_NAME
10.BUILD PSB=PSB_NAME, BUILD DBD=DBD_NAMES,BLDPSB=NO
11.BUILD PSB=PSB_NAME, BUILD DBD=DBD_NAMES,BLDPSB=YES
12.BUILD PSB=PSB_NAME, BUILD DBD=DBD_NAME,BLDPSB=YES, COMP='PRECOMP'
13.BUILD PSB=PSB_NAME, BUILD DBD=DBDNAME,BLDPSB=YES, COMP='POSTCOMP'
14.BUILD PSB=PSB_NAME, BUILD DBD=DBDNAME,BLDPSB=YES, COMP='PRECOMP,POSTCOMP'
15. Multi line - for PSB and DBD - longer than single line - TOOD
16. test with list - TODO
"""

# check in acblib if the member exists - dataset member exists (zos_dataset)
def validate_build(hosts, psb_name, dbd_name, psb_lib, 
dbd_lib, acb_lib, steplib, res_lib, 
comp, bld_psb, command_input='BUILD'):
    response = hosts.all.ims_acb_gen(
        command_input=command_input,
        psb_name=psb_name,
        dbd_name=dbd_name,
        psb_lib=psb_lib,
        dbd_lib=dbd_lib,
        acb_lib=acb_lib,
        steplib=steplib,
        res_lib=res_lib,
        comp=comp,
        bld_psb=bld_psb)
    print("Result:", response)
    for result in response.contacted.values():
        pprint(result)
        print("Changed:", result['changed'])
        print("Return code:", result['rc'])
        assert result['changed'] == True
        assert result['rc'] <= '4'


def validate_delete(hosts, psb_name, dbd_name, psb_lib, dbd_lib, acb_lib, steplib, 
             res_lib, comp, command_input="DELETE"):
    response = hosts.all.ims_acb_gen(
        command_input=command_input,
        psb_name=psb_name,
        dbd_name=dbd_name,
        psb_lib=psb_lib,
        dbd_lib=dbd_lib,
        acb_lib=acb_lib,
        steplib=steplib,
        res_lib=res_lib,
        comp=comp)
    print("Result:", response)
    for result in response.contacted.values():
        pprint(result)
        print("Changed:", result['changed'])
        print("Return code: ", result['rc'])
        assert result['changed'] == True 
        assert result['rc'] <= '4'
 
def test_dbd_gen_build_psbName_all(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, PSB_NAME_ALL, None, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None, True)


def test_dbd_gen_delete_psbName(ansible_zos_module):
    hosts = ansible_zos_module
    validate_delete(hosts, PSB_NAME, None, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None)


def test_dbd_gen_build_psbName(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, PSB_NAME, None, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None, True)

# #DELETE DBD=(DBFSAMD3)
def test_dbd_gen_delete_dbdName(ansible_zos_module):
    hosts = ansible_zos_module
    validate_delete(hosts, None, DBD_NAME, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None)

# #BUILD DBD=(HOSPVARD),BLDPSB=NO
def test_dbd_gen_build_dbdName_bldPsb_no(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, None, "HOSPVARD", PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None, False)


def test_dbd_gen_build_dbdName_bldPsb_yes(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, None, "HOSPVARD", PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None, True)


def test_dbd_gen_build_psbName2(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, PSB_NAME, None, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None, True)


#DELETE PSB=(PSBGENL)\n'
#DELETE DBD=("DH41SK01", "HOSPVARD")\n'
# rc: '0'``
#   ret_code:
#     code: 0
#     msg: CC 0000
#     msg_code: '0000'
#     msg_txt: '' ->
# check in acblib if this member got deleted 
def test_dbd_gen_delete_psbName_dbdName(ansible_zos_module):
    hosts = ansible_zos_module
    validate_delete(hosts, PSB_NAME, DBD_NAMES, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None)


def test_dbd_gen_build_psbName3(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, PSB_NAME, None, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None, True)


def test_dbd_gen_build_psbName_dbdNames_bldPsb_no(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, PSB_NAME, DBD_NAMES, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None, False)


def test_dbd_gen_build_psbName_dbdNames_bldPsb_yes(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, PSB_NAME, DBD_NAMES, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, None, True)


def test_dbd_gen_build_psbName_dbdName_bldPsb_yes_comp_precomp(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, PSB_NAME, None, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, COMP_PRE, True)


def test_dbd_gen_build_psbName_dbdName_bldPsb_yes_comp_postcomp(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, PSB_NAME, None, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, COMP_POST, True)


def test_dbd_gen_build_psbName_dbdName_bldPsb_yes_comp_precomp_postcomp(ansible_zos_module):
    hosts = ansible_zos_module
    validate_build(hosts, PSB_NAME, None, PSBLIB, DBDLIB, ACBLIB, STEPLIB, RESLIB, COMP, True)


