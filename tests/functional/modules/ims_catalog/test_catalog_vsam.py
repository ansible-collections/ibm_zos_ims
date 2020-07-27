import pytest

from pprint import pprint
from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import CatalogInputParameters as cp # pylint: disable=import-error
from ibm_zos_ims.tests.functional.module_utils.ims_test_catalog_utils import load_catalog, purge_catalog # pylint: disable=import-error
from ibm_zos_ims.tests.functional.module_utils.ims_test_gen_utils import PSBInputParameters as ps # pylint: disable=import-error
from ibm_zos_ims.tests.functional.module_utils.ims_test_gen_utils import DBDInputParameters as db # pylint: disable=import-error
from ibm_zos_ims.tests.functional.module_utils.ims_test_gen_utils import ACBInputParameters as ac # pylint: disable=import-error

def test_gen_vsam_acb_stage_import(ansible_zos_module):
  hosts = ansible_zos_module
  
  # # Load the catalog
  # load_catalog(hosts, 
  #             psb_lib=cp.PSBLIB, 
  #             dbd_lib=cp.DBDLIB, 
  #             acb_lib=cp.ACBLIB, 
  #             steplib=cp.STEPLIB, 
  #             reslib=cp.RESLIB, 
  #             proclib=cp.PROCLIB, 
  #             primary_log_dataset=cp.PRIMARYLOG, 
  #             buffer_pool_param_dataset=cp.BUFFERPOOL, 
  #             mode=cp.LOADMODE,
  #             validation_msg="DFS4434I",
  #             control_statements={
  #               'managed_acbs': {
  #                 'setup': True
  #               }
  #             })

  # # Generate vsam PSB
  # response = hosts.all.ims_psb_gen(src=ps.SOURCE, location="DATA_SET", replace=True, member_list=['PGSAM1'], psb_name=None, dest=ps.DESTINATION, sys_lib=["IMSBLD.I15RTSMM.SDFSMAC", "SYS1.MACLIB"])
  # for result in response.contacted.values():
  #     pprint(result)
  #     print("Changed:", result['changed'])
  #     assert result['changed'] == True
  #     assert result['rc'] == 0
  #     # Check for success message (if we remove return codes)
  #     assert result['msg'] == 'PSBGEN execution was successful.'
  
  #Add to ACBLIB
  response = hosts.all.ims_acb_gen(hosts, command_input=ac.COMMAND_INPUT_BUILD, psb_name=ac.PSB_NAME, psb_lib=ac.PSBLIB, dbd_lib=ac.DBDLIB, acb_lib=ac.ACBLIB, steplib=ac.STEPLIB, reslib=ac.RESLIB)
  print("Result:", response)
  for result in response.contacted.values():
    pprint(result)
    print("Changed:", result.get('changed'))
    print("Return code:", result.get('rc'))
    assert result.get('changed') == True
    assert result.get('rc') <= 4

  # # Add to the catalog
  # load_catalog(hosts, 
  #             psb_lib=cp.PSBLIB, 
  #             dbd_lib=cp.DBDLIB, 
  #             acb_lib=cp.ACBLIB, 
  #             steplib=cp.STEPLIB, 
  #             reslib=cp.RESLIB, 
  #             proclib=cp.PROCLIB, 
  #             primary_log_dataset=cp.PRIMARYLOG, 
  #             buffer_pool_param_dataset=cp.BUFFERPOOL, 
  #             mode=cp.UPDATEMODE,
  #             validation_msg="DFS4434I",
  #             control_statements={
  #               'managed_acbs': {
  #                 'stage': {
  #                     'save_acb': "LATEST",
  #                 }
  #               }
  #             })


