# -*- coding: utf-8 -*-

import pytest

from pprint import pprint
from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import CatalogInputParameters as cp # pylint: disable=import-error
from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import load_catalog, purge_catalog # pylint: disable=import-error

# Scenario that tests catalog analysis mode
def test_catalog_purge_analysis(ansible_zos_module):
  hosts = ansible_zos_module
  purge_catalog(hosts, 
                psb_lib=cp.PSBLIB, 
                dbd_lib=cp.DBDLIB, 
                steplib=cp.STEPLIB, 
                reslib=cp.RESLIB, 
                proclib=cp.PROCLIB, 
                primary_log_dataset=cp.PRIMARYLOG, 
                buffer_pool_param_dataset=cp.BUFFERPOOL, 
                mode=cp.ANALYSISMODE,
                validation_msg="DFS4430I",
                changed=False
                )

# Scenario that tests updating of retention criteria
def test_catalog_update_retention(ansible_zos_module):
  hosts = ansible_zos_module

  load_catalog(hosts, 
                psb_lib=cp.PSBLIB, 
                dbd_lib=cp.DBDLIB, 
                acb_lib=cp.ACBLIB, 
                steplib=cp.STEPLIB, 
                reslib=cp.RESLIB, 
                proclib=cp.PROCLIB, 
                primary_log_dataset=cp.PRIMARYLOG, 
                buffer_pool_param_dataset=cp.BUFFERPOOL, 
                mode=cp.LOADMODE,
                validation_msg="DFS4434I")

  purge_catalog(hosts, 
                psb_lib=cp.PSBLIB, 
                dbd_lib=cp.DBDLIB, 
                steplib=cp.STEPLIB, 
                reslib=cp.RESLIB, 
                proclib=cp.PROCLIB, 
                primary_log_dataset=cp.PRIMARYLOG, 
                buffer_pool_param_dataset=cp.BUFFERPOOL, 
                mode=cp.ANALYSISMODE,
                update_retention_criteria=cp.RETENTION,
                validation_msg="UPDATE DBD",
                changed=False
                )
  
  purge_catalog(hosts, 
                psb_lib=cp.PSBLIB, 
                dbd_lib=cp.DBDLIB, 
                steplib=cp.STEPLIB, 
                reslib=cp.RESLIB, 
                proclib=cp.PROCLIB, 
                primary_log_dataset=cp.PRIMARYLOG, 
                buffer_pool_param_dataset=cp.BUFFERPOOL, 
                mode=cp.PURGEMODE,
                validation_msg="DFS4518I",
                delete=cp.DELETES)