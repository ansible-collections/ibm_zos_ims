# -*- coding: utf-8 -*-

import pytest
from pprint import pprint

from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import CatalogInputParameters as cp # pylint: disable=import-error
from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import load_catalog, purge_catalog # pylint: disable=import-error

# Scenario 4: Invalid mode option=load, managed_acbs with stage 
def test_catalog_load_managed_acbs(ansible_zos_module):
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
                validation_msg="You cannot update or stage ACBs in catalog LOAD mode.",
                control_statements={
                    'managed_acbs':{
                        'stage': {
                        'save_acb': "UNCOND",
                        'clean_staging_dataset': True
                    }
                    }
                })