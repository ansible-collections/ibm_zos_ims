import pytest
from pprint import pprint


def load_catalog(hosts, validation_msg, mode, psb_lib, dbd_lib, steplib, reslib, proclib, primary_log_dataset,
          buffer_pool_param_dataset, acb_lib, online_batch=None, dbrc=None, ims_id=None, irlm_id=None, control_statements=None, bootstrap_dataset=None, 
          directory_dataset=None, temp_acb_dataset=None, directory_staging_dataset=None, 
          secondary_log_dataset=None, sysabend=None, check_timestamp=None):

    response = hosts.all.ims_catalog_populate(
        online_batch=online_batch,
        dbrc=dbrc,
        ims_id=ims_id,
        irlm_id=irlm_id,
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
          buffer_pool_param_dataset, online_batch=None, dbrc=None, ims_id=None, irlm_id=None, sysut1=None, update_retention_criteria=None,
          delete=None, managed_acbs=None, delete_dbd_by_version=None, resource_chkp_freq=None, mode='PURGE'):
    
    response = hosts.all.ims_catalog_purge(
        online_batch=online_batch,
        dbrc=dbrc,
        ims_id=ims_id,
        irlm_id=irlm_id,
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




class CatalogInputParameters():
  PSBLIB = ["IMSTESTL.IMS1.PSBLIB"]
  DBDLIB = ["IMSTESTL.IMS1.DBDLIB"]
  ACBLIB = ["IMSTESTL.IMS1.ACBLIB"]
  STEPLIB = ["IMSTESTL.IMS1.SDFSRESL"]
  PROCLIB = "IMSTESTL.IMS1.PROCLIB"
  RESLIB = ["IMSTESTL.IMS1.SDFSRESL"]    
  BUFFERPOOL = "IMSTESTL.IMS1.PROCLIB(DFSVSMHP)"
  LOADMODE = "LOAD"
  UPDATEMODE = "UPDATE"
  PRIMARYLOG = {
    "dataset_name": "IMSTESTU.IMS1.LOG2",
    "disposition": "NEW",
    "normal_disposition": "DELETE",
    "record_format": "FB",
    "record_length": "4092",
    "block_size": "4096",
    "primary": "100",
    "primary_unit": "CYL",
    "secondary": "75",
    "secondary_unit": "CYL",
    "type": "SEQ"
  }
  PURGEMODE = "PURGE"
  DELETES=[
    { 
      "resource": "DBD",
      "member_name": "DB*",
      "time_stamp": '*'
    },
    { 
      "resource": "DBD",
      "member_name": "AUTO*",
      "time_stamp": '*'
    },
    { 
      "resource": "DBD",
      "member_name": "DF*",
      "time_stamp": '*'
    },
    { 
      "resource": "DBD",
      "member_name": "DI*",
      "time_stamp": '*'
    },
    { 
      "resource": "DBD",
      "member_name": "EMP*",
      "time_stamp": '*'
    },
    { 
      "resource": "DBD",
      "member_name": "IP*",
      "time_stamp": '*'
    },
    { 
      "resource": "DBD",
      "member_name": "IV*",
      "time_stamp": '*'
    },
    { 
      "resource": "DBD",
      "member_name": "SI*",
      "time_stamp": '*'
    },
    { 
      "resource": "PSB",
      "member_name": "AUT*",
      "time_stamp": '*'
    },
    { 
      "resource": "PSB",
      "member_name": "DBF*",
      "time_stamp": '*'
    },
     { 
      "resource": "PSB",
      "member_name": "DFH*",
      "time_stamp": '*'
    },
     { 
      "resource": "PSB",
      "member_name": "DFSI*",
      "time_stamp": '*'
    },
     { 
      "resource": "PSB",
      "member_name": "IP*",
      "time_stamp": '*'
    }
    
  ]