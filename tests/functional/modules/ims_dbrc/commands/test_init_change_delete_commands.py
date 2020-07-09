# -*- coding: utf-8 -*-

from pprint import pprint
import pytest
from ibm_zos_ims.tests.functional.module_utils.ims_test_gen_utils import DBRCInputParameters as ip # pylint: disable=import-error
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.ims_module_error_messages import DBRCErrorMessages as em # pylint: disable=import-error
__metaclass__ = type


def test_delete_db_for_clean_up_before(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command=["DELETE.DB DBD(TESTDB)"],
        steplib=ip.STEPLIB, dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
        recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
    )
    for result in results.contacted.values():
        pprint(result)

def test_init_db_command(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command=["INIT.DB DBD(TESTDB) SHARELVL(1) TYPEFP"],
        steplib=ip.STEPLIB, dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
        recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
    )
    for result in results.contacted.values():
        pprint(result)
        assert result['msg'] == em.SUCCESS_MSG


def test_genjcl_image_copy_command(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command=["CHANGE.DB DBD(TESTDB) ALTER NOAUTH ICREQ  TYPEIMS NORAND"],
        # command=["GENJCL.IC DBD(TESTDB) COPIES(1)"],
        steplib=ip.STEPLIB, dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
        recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
    )
    for result in results.contacted.values():
        pprint(result)
        assert result['msg'] == em.SUCCESS_MSG

def test_delete_db_for_clean_up_after(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command=["DELETE.DB DBD(TESTDB)"],
        steplib=ip.STEPLIB, dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
        recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
    )
    for result in results.contacted.values():
        pprint(result)
        assert result['msg'] == em.SUCCESS_MSG

def test_db_random(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command=["DELETE.LOG STARTIME(07054121212023456) INTERIM"],
        steplib=ip.STEPLIB, dbdlib=ip.DBDLIB, genjcl=ip.GENJCL,
        recon1=ip.RECON1, recon2=ip.RECON2, recon3=ip.RECON3
    )
    for result in results.contacted.values():
        pprint(result)
        assert result['msg'] == em.SUCCESS_MSG