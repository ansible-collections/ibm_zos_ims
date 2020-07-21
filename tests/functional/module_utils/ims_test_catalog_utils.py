class CatalogInputParameters():
  PSBLIB = ["IMSTESTL.IMS1.PSBLIB"]
  DBDLIB = ["IMSTESTL.IMS1.DBDLIB"]
  ACBLIB = ["IMSTESTL.IMS1.ACBLIB"]
  STEPLIB = ["IMSTESTL.IMS1.SDFSRESL"]
  PROCLIB = 'IMSTESTL.IMS1.PROCLIB'
  RESLIB = ["IMSTESTL.IMS1.SDFSRESL"]
  BUFFERPOOL = "IMSTESTL.IMS1.PROCLIB(DFSVSMHP)"
  LOADMODE = "LOAD"
  UPDATEMODE = "UPDATE"
  PRIMARYLOG = {
    "dataset_name": "IMSTESTL.IMS1.LOG1",
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