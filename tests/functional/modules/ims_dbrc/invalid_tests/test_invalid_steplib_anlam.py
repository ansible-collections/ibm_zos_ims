# -*- coding: utf-8 -*-

from pprint import pprint
import pytest
from ibm_zos_ims.tests.functional.module_utils.ims_test_dbrc_utils import DBRCInputParameters as ip # pylint: disable=import-error
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.ims_module_error_messages import DBRCErrorMessages as em # pylint: disable=import-error

__metaclass__ = type

"""
Author: An Lam
"""

def test_missing_steplib(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command="LIST.RECON STATUS",
        dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
        recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
    )
    for result in results.contacted.values():
        pprint(result)
        assert result['msg'] == em.MISSING_STEPLIB

def test_missing_steplib2(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command="LIST.DB ALL",
        dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
        recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
    )
    for result in results.contacted.values():
        pprint(result)
        assert result['msg'] == em.MISSING_STEPLIB

def test_missing_all_recon(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command="LIST.RECON STATUS",
        steplib=ip.STEPLIB,
        dbdlib=ip.DBDLIB, genjcl=ip.GENJCL
    )
    for result in results.contacted.values():
        pprint(result)
        print("+++ result[msg] = ", result['msg'])
        assert result['msg'].find(em.DYNALLOC_RECON_REQUIREMENT_MSG) != -1

def test_missing_all(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command="",
    )
    for result in results.contacted.values():
        pprint(result)
        assert result['msg'] == em.MISSING_STEPLIB

# def test_dup_params(ansible_zos_module):
#     hosts = ansible_zos_module
#     results = hosts.all.ims_dbrc(
#         command="LIST.RECON STATUS",
#         dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
#         recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3,
#         command="LIST.RECON STATUS",
#         dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
#         recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
#     )
#     for result in results.contacted.values():
#         pprint(result)
#         assert result['msg'] == em.MISSING_STEPLIB

def test_single_invalid_steplib(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command="LIST.RECON STATUS",
        steplib=["IMSTESTL.INVALID.STEPLIB"], dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
        recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
    )
    error_message = "Unable to load program DSPURX00"
    for result in results.contacted.values():
        pprint(result)
        assert error_message in result['msg']

def test_single_invalid_steplib2(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command="LIST.DB ALL",
        steplib=["IMSTESTL.INVALID.STEPLIB"], dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
        recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
    )
    error_message = "Unable to load program DSPURX00"
    for result in results.contacted.values():
        pprint(result)
        assert error_message in result['msg']

def test_invalid_steplib_with_valid_steplib(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command="LIST.RECON STATUS",
        steplib=ip.STEPLIB + ["IMSTESTL.INVALID.STEPLIB"], dbdlib=ip.DBDLIB,
        genjcl="IMSTESTL.IMS1.PROCLIB",
        recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
    )
    for result in results.contacted.values():
        pprint(result)

