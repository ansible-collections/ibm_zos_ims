# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
import pytest
from pprint import pprint
import sys
# sys.path.append("/Users/pedrotrevino/Desktop/Coding/stephanie_zos_ibm_ims/ibm_zos_ims")

from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import CatalogInputParameters as cp  # pylint: disable=import-error
from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import load_catalog, purge_catalog  # pylint: disable=import-error
__metaclass__ = type


# 1 - In populate test case, we use the valid default case for the module
def test_populate_valid_default(ansible_zos_module):
    hosts = ansible_zos_module
    load_catalog(hosts,
                 psb_lib=cp.PSBLIB,
                 dbd_lib=cp.DBDLIB,
                 acb_lib=cp.ACBLIB,
                 steplib=cp.STEPLIB,
                 reslib=cp.RESLIB,
                 proclib=cp.PROCLIB,
                 modstat=cp.MODSTAT,
                 primary_log_dataset=cp.PRIMARYLOG,
                 buffer_pool_param_dataset=cp.BUFFERPOOL,
                 dfsdf_member="CAT",
                 mode=cp.LOADMODE,
                 validation_msg="",
                 rc=0
                 ) 
    
# 2 - In purge test case, we use the valid default case for the module
def test_purge_valid_default(ansible_zos_module):
    hosts = ansible_zos_module
    purge_catalog(hosts,
                  psb_lib=cp.PSBLIB,
                  dbd_lib=cp.DBDLIB,
                  steplib=cp.STEPLIB,
                  reslib=cp.RESLIB,
                  proclib=cp.PROCLIB,
                  primary_log_dataset=cp.PRIMARYLOG,
                  buffer_pool_param_dataset=cp.BUFFERPOOL,
                  dfsdf_member="CAT",
                  mode=cp.PURGEMODE,
                  validation_msg="",
                  sysut1=cp.SYSUT1,
                  rc=0,
                  delete=cp.DELETES)


