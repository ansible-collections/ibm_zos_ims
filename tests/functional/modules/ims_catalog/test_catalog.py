# -*- coding: utf-8 -*-

import pytest
from pprint import pprint

from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import CatalogInputParameters as cp # pylint: disable=import-error

def load_catalog(hosts, validation_msg, mode, psb_lib, dbd_lib, steplib, reslib, proclib, primary_log_dataset,
          buffer_pool_param_dataset, acb_lib, irlm_enabled=None, irlm_id=None, control_statements=None, bootstrap_dataset=None, 
          directory_dataset=None, temp_acb_dataset=None, directory_staging_dataset=None, 
          secondary_log_dataset=None, sysabend=None, check_timestamp=None):

    response = hosts.all.ims_catalog_populate(
        irlm_id=irlm_id,
        irlm_enabled=irlm_enabled,
        psb_lib=psb_lib,
        dbd_lib=dbd_lib,
        acb_lib=acb_lib,
        steplib=steplib,
        reslib=reslib,
        proclib=proclib,
        sysabend=sysabend,
        check_timestamp=check_timestamp,
        buffer_pool_param_dataset=buffer_pool_param_dataset,
        mode=mode,
        control_statements=control_statements,
        bootstrap_dataset=bootstrap_dataset,
        directory_datasets=directory_dataset,
        temp_acb_dataset=temp_acb_dataset,
        directory_staging_dataset=directory_staging_dataset,
        primary_log_dataset=primary_log_dataset,
        secondary_log_dataset=secondary_log_dataset
        )
    for result in response.contacted.values():
        pprint(result)
        print("Changed:", result['changed'])
        assert result['changed'] == False
        assert result['rc'] == 0
        assert validation_msg in result['content']

def purge_catalog(hosts, validation_msg, primary_log_dataset, psb_lib, dbd_lib, steplib, reslib, proclib,
          buffer_pool_param_dataset, irlm_enabled=None, irlm_id=None, sysut1=None, update_retention_criteria=None,
          delete=None, managed_acbs=None, delete_dbd_by_version=None, resource_chkp_freq=None, mode='PURGE'):
    
    response = hosts.all.ims_catalog_purge(
        irlm_id=irlm_id,
        irlm_enabled=irlm_enabled,
        psb_lib=psb_lib,
        dbd_lib=dbd_lib,
        steplib=steplib,
        resource_chkp_freq=resource_chkp_freq,
        reslib=reslib,
        proclib=proclib,
        update_retention_criteria=update_retention_criteria,
        delete_dbd_by_version=delete_dbd_by_version,
        buffer_pool_param_dataset=buffer_pool_param_dataset,
        mode=mode,
        primary_log_dataset=primary_log_dataset,
        delete=delete,
        managed_acbs=managed_acbs,
        sysut1=sysut1
        )
    for result in response.contacted.values():
        pprint(result)
        print("Changed:", result['changed'])
        assert result['changed'] == False
        assert result['rc'] == 0
        assert validation_msg in result['content']


def test_catalog_load_simple(ansible_zos_module):
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
                mode=cp.PURGEMODE,
                validation_msg="DFS4518I",
                delete=cp.DELETES)

    

