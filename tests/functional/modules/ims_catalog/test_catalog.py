import pytest
from pprint import pprint

def load_catalog(hosts, psb_lib, dbd_lib, steplib, reslib, proclib, sysabend,
          buffer_pool_param_dataset, acb_lib, control_statements, bootstrap_dataset, 
          directory_dataset, temp_acb_dataset, directory_staging_dataset, 
          primary_log_dataset, secondary_log_dataset, mode='LOAD', validation_msg):

    response = hosts.all.ims_catalog_populate(
        psb_lib=psb_lib,
        dbd_lib=dbd_lib,
        acb_lib=acb_lib,
        steplib=steplib,
        reslib=reslib,
        proclib=proclib,
        sysabend=sysabend,
        buffer_pool_param_dataset=buffer_pool_param_dataset,
        mode=mode,
        control_statements=control_statements,
        bootstrap_dataset=bootstrap_dataset,
        directory_dataset=directory_dataset,
        temp_acb_dataset=temp_acb_dataset,
        directory_staging_dataset=directory_staging_dataset,
        primary_log_dataset=primary_log_dataset,
        secondary_log_dataset=secondary_log_dataset
        )
    for result in response.contacted.values():
        pprint(result)
        print("Changed:", result['changed'])
        assert result['changed'] == False
        assert result['rc'] != 0
        assert validation_msg in result['content']

def update_catalog(hosts, psb_lib, dbd_lib, steplib, reslib, proclib, sysabend,
          buffer_pool_param_dataset, acb_lib, control_statements, bootstrap_dataset, 
          directory_dataset, temp_acb_dataset, directory_staging_dataset, 
          primary_log_dataset, secondary_log_dataset, mode='LOAD', validation_msg):
    
     response = hosts.all.ims_catalog_populate(
        psb_lib=psb_lib,
        dbd_lib=dbd_lib,
        acb_lib=acb_lib,
        steplib=steplib,
        reslib=reslib,
        proclib=proclib,
        sysabend=sysabend,
        buffer_pool_param_dataset=buffer_pool_param_dataset,
        mode=mode,
        control_statements=control_statements,
        bootstrap_dataset=bootstrap_dataset,
        directory_dataset=directory_dataset,
        temp_acb_dataset=temp_acb_dataset,
        directory_staging_dataset=directory_staging_dataset,
        primary_log_dataset=primary_log_dataset,
        secondary_log_dataset=secondary_log_dataset
        )
    for result in response.contacted.values():
        pprint(result)
        print("Changed:", result['changed'])
        assert result['changed'] == False
        assert result['rc'] != 0
        assert validation_msg in result['content']

def purge_catalog(hosts, psb_lib, dbd_lib, steplib, reslib, proclib, sysabend,
          buffer_pool_param_dataset, acb_lib, sysut1, update_retention_criteria,
          delete, managed_acbs, primary_log_dataset,mode , validation_msg):
    
     response = hosts.all.ims_catalog_populate(
        psb_lib=psb_lib,
        dbd_lib=dbd_lib,
        acb_lib=acb_lib,
        steplib=steplib,
        reslib=reslib,
        proclib=proclib,
        sysabend=sysabend,
        buffer_pool_param_dataset=buffer_pool_param_dataset,
        mode=mode,
        control_statements=control_statements,
        bootstrap_dataset=bootstrap_dataset,
        directory_dataset=directory_dataset,
        temp_acb_dataset=temp_acb_dataset,
        directory_staging_dataset=directory_staging_dataset,
        primary_log_dataset=primary_log_dataset,
        secondary_log_dataset=secondary_log_dataset
        )
    for result in response.contacted.values():
        pprint(result)
        print("Changed:", result['changed'])
        assert result['changed'] == False
        assert result['rc'] != 0
        assert validation_msg in result['content']
