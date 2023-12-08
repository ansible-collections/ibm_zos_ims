# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
import pytest
from pprint import pprint
from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import CatalogInputParameters as cp  # pylint: disable=import-error
from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import load_catalog, purge_catalog  # pylint: disable=import-error

__metaclass__ = type

# Simple scenario that loads the catalog without managed acb datasets and purges it

def test_catalog_create_datasets_01(ansible_zos_module):
   hosts = ansible_zos_module
   response = hosts.all.zos_data_set(name="IMSTESTL.IMS1.DFSCD000.DI1001", state="present", volume="222222", primary="200")

def test_catalog_create_datasets_02(ansible_zos_module):
   hosts = ansible_zos_module
   response = hosts.all.zos_data_set(name="IMSTESTL.IMS1.DFSCD000.DI1002", state="present", volume="222222", primary="200")

def test_catalog_load_simple(ansible_zos_module):
    hosts = ansible_zos_module
    load_catalog(hosts,
                 psb_lib=cp.PSBLIB,
                 dbd_lib=cp.DBDLIB,
                 acb_lib=cp.ACBLIB,
                 steplib=cp.STEPLIB,
                 reslib=cp.RESLIB,
                 proclib=cp.PROCLIB,
                 dfsdf_member="CAT",
                 modstat=cp.MODSTAT,
                 primary_log_dataset=cp.PRIMARYLOG,
                 buffer_pool_param_dataset=cp.BUFFERPOOL,
                 mode=cp.LOADMODE,
                 validation_msg="")  # Don't check for a message since the message is different depending on the configuration

    purge_catalog(hosts,
                  psb_lib=cp.PSBLIB,
                  dbd_lib=cp.DBDLIB,
                  steplib=cp.STEPLIB,
                  reslib=cp.RESLIB,
                  proclib=cp.PROCLIB,
                  dfsdf_member="CAT",
                  primary_log_dataset=cp.PRIMARYLOG,
                  buffer_pool_param_dataset=cp.BUFFERPOOL,
                  mode=cp.PURGEMODE,
                  validation_msg="DFS4518I",
                  # validation_msg="",
                  sysut1=cp.SYSUT1,
                  delete=cp.DELETES)
