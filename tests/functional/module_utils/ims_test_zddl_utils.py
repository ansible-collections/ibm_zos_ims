from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

class ZDDLInputParameters():
#     JOB_CARD = """//ANSIBLE JOB 'testing',
# //  CLASS=A,MSGLEVEL=(1,1),REGION=0M,
# //  MSGCLASS=H,NOTIFY=&SYSUID"""
    ONLINE = True
    OFFLINE = False
    IMS_ID = "IMS1" # Check if this is correct
    IRLM_ID = "IMS1"
    STEPLIB = ["IMSTESTL.IMS1.SDFSRESL"]
    RESLIB = ["IMSTESTL.IMS1.SDFSRESL"]
    PROCLIB = ["IMSTESTL.IMS1.PROCLIB"]
    SQL_INPUT = "CREATE DATABASE SVL1;"
    SQL_INPUTS = ["CREATE DATABASE SVL2;",
                  "CREATE TABLE IMS1(DB INT PRIMARY KEY) IN DATABASE SVL2;",
                  "COMMIT DDL;"
                  ]



    SQL_FULL_INPUTS = [ "CREATE DATABASE DEMODB1;",
                        "CREATE TABLE T1(C1 INT PRIMARY KEY);",
                        "USER.DDL(TESTDB02)",
                        "USER.DDL(TESTDB03)",
                        "DROP PROGRAMVIEW DEMOPSB1 IF EXISTS;",
                        "CREATE PROGRAMVIEW DEMOPSB1",
                        "(CREATE SCHEMA S1 USING DEMODB1 AS S1",
                        "(CREATE SENSEGVIEW T1)",
                        ") LANGASSEM;"
                       ]

    VERBOSE = False
    AUTO_COMMIT = False
    SIMULATE = False
    DYNAMIC_PROGRAMVIEW = False # All the Control statements are false as default, even though create_programview is the only one specified as default
    # INVALID VALUES
    INVALID_IMS_ID = "INVALID"
    INVALID_IRLM_ID = "INVALID"
    INVALID_STEPLIB = ["INVALID.SDFSRESL"]
    INVALID_RESLIB = ["INVALID.SDFSRESL"]
    INVALID_PROCLIB = ["INVALID.PROCLIB"]
    INVALID_SQL_INPUT = ["jhhhjjbnjbhjbi"]
    MIXED_SQL_INPUT =[  "CREATE DATABASE SVL1;",
                        "CREATE TABLE IMS1(DB INT PRIMARY KEY) IN DATABASE SVL1;",
                        "njdsnfjsndjfgsfng"]
    EMPTY_STEPLIB = "IMSTESTL.ANS.EMPTY.STEPLIB"
    EMPTY_SQL_INPUT = []
