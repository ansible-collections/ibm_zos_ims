# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
import pytest
from pprint import pprint

from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import CatalogInputParameters as cp  # pylint: disable=import-error
from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import load_catalog, purge_catalog  # pylint: disable=import-error

__metaclass__ = type

"""
Scenario 4: Invalid mode option=load, managed_acbs with stage
"""


def test_catalog_stage_managed_acbs_in_update(ansible_zos_module):
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
                 dfsdf_member=cp.DFSDF_DEFAULT,
                 mode=cp.LOADMODE,
                 validation_msg="You cannot update or stage ACBs in catalog LOAD mode.",
                 rc=1,
                 changed=False,
                 control_statements={
                     'managed_acbs': {
                         'stage': {
                             'save_acb': "UNCOND",
                             'clean_staging_dataset': True
                         }
                     }
                 })


"""
Scenario 5: Tests a catalog update mode while specifying managedacbs update or stage.
It then tries to specify the bootstrap dataset, or the directory datasets, or the directory
staging datasets. The ansible module should throw an error as this is not allowed. (test
with disposition share, this may be allowed).
"""


def test_catalog_update_mode_boostrap_data_set(ansible_zos_module):
    hosts = ansible_zos_module
    bootstrap_data_set = {
        'dataset_name': cp.BSDS,
        'disposition': 'SHR',
        'normal_disposition': 'CATLG',
        'primary': 350,
        'volumes': ['222222']
    }
    load_catalog(hosts,
                 psb_lib=cp.PSBLIB,
                 dbd_lib=cp.DBDLIB,
                 acb_lib=cp.ACBLIB,
                 steplib=cp.STEPLIB,
                 reslib=cp.RESLIB,
                 proclib=cp.PROCLIB,
                 primary_log_dataset=cp.PRIMARYLOG,
                 bootstrap_dataset=bootstrap_data_set,
                 buffer_pool_param_dataset=cp.BUFFERPOOL,
                 dfsdf_member=cp.DFSDF_DEFAULT,
                 mode=cp.UPDATEMODE,
                 validation_msg="You cannot define directory datasets, the bootstrap dataset, "
                                "or directory staging datasets with MANAGEDACBS=STAGE or MANAGEDACBS=UPDATE",
                 rc=1,
                 changed=False,
                 control_statements={
                     'managed_acbs': {
                         'stage': {
                             'save_acb': "UNCOND",
                             'clean_staging_dataset': True
                         }
                     }
                 })


def test_catalog_update_mode_directory_data_set(ansible_zos_module):
    hosts = ansible_zos_module
    directory_data_sets = [
        {
            'dataset_name': cp.DIR1,
            'disposition': 'NEW',
            'normal_disposition': 'CATLG',
            'primary': 200,
            'volumes': ['222222']
        },
        {
            'dataset_name': cp.DIR2,
            'disposition': 'NEW',
            'normal_disposition': 'CATLG',
            'primary': 200,
            'volumes': ['222222']
        },
    ]
    load_catalog(hosts,
                 psb_lib=cp.PSBLIB,
                 dbd_lib=cp.DBDLIB,
                 acb_lib=cp.ACBLIB,
                 steplib=cp.STEPLIB,
                 reslib=cp.RESLIB,
                 proclib=cp.PROCLIB,
                 primary_log_dataset=cp.PRIMARYLOG,
                 directory_datasets=directory_data_sets,
                 buffer_pool_param_dataset=cp.BUFFERPOOL,
                 dfsdf_member=cp.DFSDF_DEFAULT,
                 mode=cp.UPDATEMODE,
                 validation_msg="You cannot define directory datasets, the bootstrap dataset, "
                                "or directory staging datasets with MANAGEDACBS=STAGE or MANAGEDACBS=UPDATE",
                 rc=1,
                 changed=False,
                 control_statements={
                     'managed_acbs': {
                         'stage': {
                             'save_acb': "UNCOND",
                             'clean_staging_dataset': True
                         }
                     }
                 })


def test_catalog_update_mode_directory_staging_data_set(ansible_zos_module):
    hosts = ansible_zos_module
    directory_staging_data_set = {
        'dataset_name': cp.STAGE,
        'disposition': 'NEW',
        'normal_disposition': 'CATLG',
        'primary': 300,
        'volumes': ['222222']
    }
    load_catalog(hosts,
                 psb_lib=cp.PSBLIB,
                 dbd_lib=cp.DBDLIB,
                 acb_lib=cp.ACBLIB,
                 steplib=cp.STEPLIB,
                 reslib=cp.RESLIB,
                 proclib=cp.PROCLIB,
                 primary_log_dataset=cp.PRIMARYLOG,
                 directory_staging_dataset=directory_staging_data_set,
                 buffer_pool_param_dataset=cp.BUFFERPOOL,
                 dfsdf_member=cp.DFSDF_DEFAULT,
                 mode=cp.UPDATEMODE,
                 validation_msg="You cannot define directory datasets, the bootstrap dataset, "
                                "or directory staging datasets with MANAGEDACBS=STAGE or MANAGEDACBS=UPDATE",
                 rc=1,
                 changed=False,
                 control_statements={
                     'managed_acbs': {
                         'stage': {
                             'save_acb': "UNCOND",
                             'clean_staging_dataset': True
                         }
                     }
                 })
    

"""
Scenario 6: Simple tests to check that the DFSDF member has the correct limitations for the accepted values
            for the catalog_populate module
"""

# 6.1 - In catalog populate test case, we check that the length of the dfsdf memebr can't be more than 3 characters
def test_invalid_catalog_pupolate_simple_member_length_more_tree(ansible_zos_module):
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
                 dfsdf_member="0000",
                 mode=cp.LOADMODE,
                 validation_msg="0000 is not equal to length 3",
                 rc=1
                 ) 

# 6.2 - In catalog populate test case, we check that the length of the dfsdf memebr can't be less than 3 characters
def test_invalid_catalog_pupolate_simple_member_length_less_tree(ansible_zos_module):
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
                 dfsdf_member="00",
                 mode=cp.LOADMODE,
                 validation_msg="00 is not equal to length 3",
                 rc=1
                 ) 

# 6.3 - In catalog populate test case, we check that the value of the dfsdf_member value does not contain special characters
def test_invalid_catalog_pupolate_simple_member_no_special_char(ansible_zos_module):
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
                 dfsdf_member="c1&",
                 mode=cp.LOADMODE,
                 validation_msg="dfsdf_member input cannot contain special characters, it must be alphanumeric",
                 rc=1
                 ) 

# 6.4 - In catalog populate test case, when running DLI (online_batch=false) we have to specify dfsdf_member
def test_invalid_catalog_pupolate_simple_member_dli_check(ansible_zos_module):
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
                 mode=cp.LOADMODE,
                 dfsdf_member=None,
                 validation_msg="You must specify the suffix for the DFSDFxxx member when running as DLI.",
                 rc=1
                 )

# 6.5 - In this catalog populate test case, we check that the specified member exists
def test_invalid_catalog_pupolate_unexistent_member(ansible_zos_module):
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
                 mode=cp.LOADMODE,
                 dfsdf_member="123",
                 validation_msg="dfsdf_member DFSDF123 input does not exist",
                 rc=1
                 )

# 6.6 - In catalog purge test case, we check that the length of the dfsdf memebr can't be more than 3 characters
def test_invalid_catalog_purge_simple_member_length_more_tree(ansible_zos_module):
    hosts = ansible_zos_module
    purge_catalog(hosts,
                  psb_lib=cp.PSBLIB,
                  dbd_lib=cp.DBDLIB,
                  steplib=cp.STEPLIB,
                  reslib=cp.RESLIB,
                  proclib=cp.PROCLIB,
                  primary_log_dataset=cp.PRIMARYLOG,
                  buffer_pool_param_dataset=cp.BUFFERPOOL,
                  dfsdf_member="0000",
                  mode=cp.PURGEMODE,
                  validation_msg="0000 is not equal to length 3",
                  # validation_msg="",
                  sysut1=cp.SYSUT1,
                  rc=1,
                  delete=cp.DELETES)

# 6.7 - In catalog purge test case, we check that the length of the dfsdf memebr can't be less than 3 characters
def test_invalid_catalog_purge_simple_member_length_less_tree(ansible_zos_module):
    hosts = ansible_zos_module
    purge_catalog(hosts,
                  psb_lib=cp.PSBLIB,
                  dbd_lib=cp.DBDLIB,
                  steplib=cp.STEPLIB,
                  reslib=cp.RESLIB,
                  proclib=cp.PROCLIB,
                  primary_log_dataset=cp.PRIMARYLOG,
                  buffer_pool_param_dataset=cp.BUFFERPOOL,
                  dfsdf_member="00",
                  mode=cp.PURGEMODE,
                  validation_msg="00 is not equal to length 3",
                  rc=1,
                  # validation_msg="",
                  sysut1=cp.SYSUT1,
                  delete=cp.DELETES)

# 6.8 - In catalog purge test case, we check that the value of the dfsdf_member value does not contain special characters
def test_invalid_catalog_purge_simple_member_no_special_char(ansible_zos_module):
    hosts = ansible_zos_module
    purge_catalog(hosts,
                  psb_lib=cp.PSBLIB,
                  dbd_lib=cp.DBDLIB,
                  steplib=cp.STEPLIB,
                  reslib=cp.RESLIB,
                  proclib=cp.PROCLIB,
                  primary_log_dataset=cp.PRIMARYLOG,
                  buffer_pool_param_dataset=cp.BUFFERPOOL,
                  dfsdf_member="&cc",
                  mode=cp.PURGEMODE,
                  validation_msg="dfsdf_member input cannot contain special characters, it must be alphanumeric",
                  # validation_msg="",
                  sysut1=cp.SYSUT1,
                  rc=1,
                  delete=cp.DELETES)

# 6.9 - In catalog purge test case, when running DLI (online_batch=false) we need to specify dfsdf_member
def test_invalid_catalog_purge_simple_member_dli_check(ansible_zos_module):
    hosts = ansible_zos_module
    purge_catalog(hosts,
                  psb_lib=cp.PSBLIB,
                  dbd_lib=cp.DBDLIB,
                  steplib=cp.STEPLIB,
                  reslib=cp.RESLIB,
                  proclib=cp.PROCLIB,
                  primary_log_dataset=cp.PRIMARYLOG,
                  buffer_pool_param_dataset=cp.BUFFERPOOL,
                  dfsdf_member=None,
                  mode=cp.PURGEMODE,
                  validation_msg="You must specify the suffix for the DFSDFxxx member when running as DLI.",
                  sysut1=cp.SYSUT1,
                  rc=1,
                  delete=cp.DELETES)
    


# 6.10 - In purge test case, we check that the specified member exists
def test_purge_valid_dfsdf_member_unexistent(ansible_zos_module):
    hosts = ansible_zos_module
    purge_catalog(hosts,
                  psb_lib=cp.PSBLIB,
                  dbd_lib=cp.DBDLIB,
                  steplib=cp.STEPLIB,
                  reslib=cp.RESLIB,
                  proclib=cp.PROCLIB,
                  primary_log_dataset=cp.PRIMARYLOG,
                  buffer_pool_param_dataset=cp.BUFFERPOOL,
                  dfsdf_member="123",
                  mode=cp.PURGEMODE,
                  validation_msg="dfsdf_member DFSDF123 input does not exist",
                  rc=1,
                  sysut1=cp.SYSUT1,
                  delete=cp.DELETES)
    