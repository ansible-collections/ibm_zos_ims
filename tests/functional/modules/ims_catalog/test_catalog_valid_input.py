# -*- coding: utf-8 -*-

import pytest
from pprint import pprint

from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import CatalogInputParameters as cp # pylint: disable=import-error
from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import load_catalog, purge_catalog # pylint: disable=import-error

# Scenario 2: Load mode, managed_acbs - setup=True
def test_catalog_load_managed_acbs(ansible_zos_module):
    
    hosts = ansible_zos_module

    purge_catalog(hosts, 
                psb_lib=cp.PSBLIB, 
                dbd_lib=cp.DBDLIB, 
                steplib=cp.STEPLIB, 
                reslib=cp.RESLIB, 
                proclib=cp.PROCLIB, 
                primary_log_dataset=cp.PRIMARYLOG, 
                buffer_pool_param_dataset=cp.BUFFERPOOL, 
                mode=cp.PURGEMODE,
                validation_msg="DELETE",
                delete=cp.DELETES,
                managed_acbs=True)

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
                validation_msg="DFS4533I",
                control_statements={'managed_acbs':{"setup":True}})

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
                delete=cp.DELETES,
                managed_acbs=True)

# Scenario 3: Update mode, managed_acbs - stage options(save_acb=UNCOND and clean_staging_dataset=True)
# and update option(replace_acb=UNCOND)
def test_catalog_update_managed_acbs_stage_and_update(ansible_zos_module):
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
                mode=cp.UPDATEMODE,
                validation_msg="DFS4536I", 
                control_statements = {
                'managed_acbs': {
                    'stage': {
                        'save_acb': "UNCOND",
                        'clean_staging_dataset': True
                    }
                }
                })
    load_catalog(hosts, 
                psb_lib=cp.PSBLIB, 
                dbd_lib=cp.DBDLIB, 
                acb_lib=cp.ACBLIB, 
                steplib=cp.STEPLIB, 
                reslib=cp.RESLIB, 
                proclib=cp.PROCLIB, 
                primary_log_dataset=cp.PRIMARYLOG, 
                buffer_pool_param_dataset=cp.BUFFERPOOL, 
                mode=cp.UPDATEMODE,
                validation_msg="DFS4534I",
                control_statements={'managed_acbs':{'update':{'replace_acb':"UNCOND"}}})

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
                delete=cp.DELETES,
                managed_acbs=True)

    

