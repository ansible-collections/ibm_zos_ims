The following is a sample input scenario of IMS DBRC commands:
```
ims_dbrc:
    command: 
        - LIST.RECON STATUS
        - LIST.DB ALL
        - LIST.DBDS DBD(CUSTOMER)
    steplib: IMSBANK.IMS1.SDFSRESL
    dynalloc: IMSTESTL.IMS1.DYNALLOC    # either provide this or the recon1/2/3 libraries
    genjcl: IMSTESTL.IMS1.GENJCL        # optional
    recon1: IMSBANK.IMS1.RECON1         # either provide these recon1/2/3 libraries or dynalloc
    recon2: IMSBANK.IMS1.RECON2
    recon3: IMSBANK.IMS1.RECON3
    dbdlib: IMSTESTL.IMS1.DBDLIB
```
There are three options for the corresponding output of the above sample input.

The first option will simply return all the output from sysprint as is. 
```
{
    "changed": "true"
    "failed": "false"
    "dbrc_output": [{
            "data": "LIST.RECON STATUS
                '--------------------------------------------------------------------------'
                RECON
                RECOVERY CONTROL DATA SET, IMS V15R1",
                DMB#=5                             INIT TOKEN=20139F1535085F
                FORCER    LOG DSN CHECK=CHECK44    STARTNEW=NO
                TAPE UNIT=          DASD UNIT=SYSALLDA  TRACEOFF   SSID=IMS1
                LIST DLOG=NO                 CA/IC/LOG DATA SETS CATALOGED=YES
                MINIMUM VERSION = 13.1       CROSS DBRC SERVICE LEVEL ID= 00002
                REORG NUMBER VERIFICATION=NO
                LOG RETENTION PERIOD=00.001 00:00:00.0
                COMMAND AUTH=NONE  HLQ=**NULL**
                RCNQUAL=**NULL**
                CATALOG=**NULL**
                ACCESS=SERIAL      LIST=STATIC
                SIZALERT DSNUM=15      VOLNUM=16     PERCENT= 95
                LOGALERT DSNUM=3       VOLNUM=16
                'TIME STAMP INFORMATION:'
                TIMEZIN = %SYS
                'OUTPUT FORMAT:  DEFAULT = LOCORG NONE   PUNC YY'
                CURRENT = LOCORG NONE   PUNC YY
                IMSPLEX = ** NONE **    GROUP ID = ** NONE **
                -DDNAME-      -STATUS-       -DATA SET NAME-
                RECON1        COPY1          IMSBANK.IMS1.RECON1
                RECON2        COPY2          IMSBANK.IMS1.RECON2
                RECON3        SPARE          IMSBANK.IMS1.RECON3
                NUMBER OF REGISTERED DATABASES =        5
                DSP0180I  NUMBER OF RECORDS LISTED IS        1
                DSP0203I  COMMAND COMPLETED WITH CONDITION CODE 00"
                DSP0220I  COMMAND COMPLETION TIME 20.139 19:48:09.753357
                DSP0211I  COMMAND PROCESSING COMPLETE
                DSP0211I  HIGHEST CONDITION CODE = 00
                DSP0058I  RML COMMAND COMPLETED
                LIST.DB ALL
                '--------------------------------------------------------------------------'
                DB
                DBD=ACCOUNT                                      DMB#=2       TYPE=IMS
                SHARE LEVEL=0               GSGNAME=**NULL**     USID=0000000001
                AUTHORIZED USID=0000000000  RECEIVE USID=0000000000 HARD USID=0000000000
                RECEIVE NEEDED USID=0000000000
                DBRCVGRP=**NULL**
                'FLAGS:                             COUNTERS:'
                BACKOUT NEEDED        =OFF         RECOVERY NEEDED COUNT   =0
                READ ONLY             =OFF         IMAGE COPY NEEDED COUNT =0
                PROHIBIT AUTHORIZATION=OFF         AUTHORIZED SUBSYSTEMS   =0
                RECOVERABLE           =YES         HELD AUTHORIZATION STATE=0
                EEQE COUNT              =0
                TRACKING SUSPENDED    =NO          RECEIVE REQUIRED COUNT  =0
                OFR REQUIRED          =NO
                REORG INTENT          =NO
                QUIESCE IN PROGRESS   =NO
                QUIESCE HELD          =NO
                '--------------------------------------------------------------------------'
                DB
                DBD=CUSTACCS                                     DMB#=3       TYPE=IMS
                SHARE LEVEL=0               GSGNAME=**NULL**     USID=0000000001
                AUTHORIZED USID=0000000000  RECEIVE USID=0000000000 HARD USID=0000000000
                RECEIVE NEEDED USID=0000000000
                DBRCVGRP=**NULL**
                'FLAGS:                             COUNTERS:'
                BACKOUT NEEDED        =OFF         RECOVERY NEEDED COUNT   =0
                READ ONLY             =OFF         IMAGE COPY NEEDED COUNT =0
                PROHIBIT AUTHORIZATION=OFF         AUTHORIZED SUBSYSTEMS   =0
                RECOVERABLE           =YES         HELD AUTHORIZATION STATE=0
                EEQE COUNT              =0
                TRACKING SUSPENDED    =NO          RECEIVE REQUIRED COUNT  =0
                OFR REQUIRED          =NO
                REORG INTENT          =NO
                QUIESCE IN PROGRESS   =NO
                QUIESCE HELD          =NO
                LIST.DBDS DBD(CUSTOMER)
                '--------------------------------------------------------------------------'
                DBDS",
                DSN=IMSBANK.IMS1.CUSTOMER.DB                                  TYPE=IMS
                DBD=CUSTOMER  DDN=CUSTOMER DSID=001 DBORG=HDAM   DSORG=OSAM
                CAGR=**NULL**  GENMAX=2     IC AVAIL=0     IC USED=0     DSSN=00000000
                NOREUSE         RECOVPD=0
                DEFLTJCL=**NULL**  ICJCL=ICJCL     OICJCL=OICJCL    RECOVJCL=RECOVJCL
                RECVJCL=ICRCVJCL
                'FLAGS:                             COUNTERS:'
                IC NEEDED      =OFF
                IC RECOMMENDED =ON
                RECOV NEEDED   =OFF
                RECEIVE NEEDED =OFF                EEQE COUNT              =0
                DSP0180I  NUMBER OF RECORDS LISTED IS        1
                DSP0203I  COMMAND COMPLETED WITH CONDITION CODE 00
                DSP0220I  COMMAND COMPLETION TIME 20.139 19:48:10.874690
                DSP0211I  COMMAND PROCESSING COMPLETE
                DSP0211I  HIGHEST CONDITION CODE = 00
                DSP0058I  RML COMMAND COMPLETED",
            "msg": "Success"
        }
    ]
}
```

Another variation of the output would be to map each individual command to it's corresponding output data. The data string will be split line by line, and return the output as an array of strings. This is shown below in the `data` fields.
```
{
    "changed": "true"
    "failed": "false"
    "dbrc_output": [{
            "command": "LIST.RECON STATUS",
            "data": [
                "LIST.RECON STATUS",
                "'--------------------------------------------------------------------------'",
                "RECON",
                "RECOVERY CONTROL DATA SET, IMS V15R1",
                "DMB#=5                             INIT TOKEN=20139F1535085F",
                "FORCER    LOG DSN CHECK=CHECK44    STARTNEW=NO",
                "TAPE UNIT=          DASD UNIT=SYSALLDA  TRACEOFF   SSID=IMS1",
                "LIST DLOG=NO                 CA/IC/LOG DATA SETS CATALOGED=YES",
                "MINIMUM VERSION = 13.1       CROSS DBRC SERVICE LEVEL ID= 00002",
                "REORG NUMBER VERIFICATION=NO",
                "LOG RETENTION PERIOD=00.001 00:00:00.0",
                "COMMAND AUTH=NONE  HLQ=**NULL**",
                "RCNQUAL=**NULL**",
                "CATALOG=**NULL**",
                "ACCESS=SERIAL      LIST=STATIC",
                "SIZALERT DSNUM=15      VOLNUM=16     PERCENT= 95",
                "LOGALERT DSNUM=3       VOLNUM=16",
                "'TIME STAMP INFORMATION:'",
                "TIMEZIN = %SYS",
                "'OUTPUT FORMAT:  DEFAULT = LOCORG NONE   PUNC YY'",
                "CURRENT = LOCORG NONE   PUNC YY",
                "IMSPLEX = ** NONE **    GROUP ID = ** NONE **",
                "-DDNAME-      -STATUS-       -DATA SET NAME-",
                "RECON1        COPY1          IMSBANK.IMS1.RECON1",
                "RECON2        COPY2          IMSBANK.IMS1.RECON2",
                "RECON3        SPARE          IMSBANK.IMS1.RECON3",
                "NUMBER OF REGISTERED DATABASES =        5",
                "DSP0180I  NUMBER OF RECORDS LISTED IS        1",
                "DSP0203I  COMMAND COMPLETED WITH CONDITION CODE 00",,
                "DSP0220I  COMMAND COMPLETION TIME 20.139 19:48:09.753357",
                "DSP0211I  COMMAND PROCESSING COMPLETE",
                "DSP0211I  HIGHEST CONDITION CODE = 00",
                "DSP0058I  RML COMMAND COMPLETED"
            ],
            "msg": "Success"
        },

        {
            "command": "LIST.DB ALL",
            "data": [
                "LIST.DB ALL",
                "'--------------------------------------------------------------------------'",
                "DB",
                "DBD=ACCOUNT                                      DMB#=2       TYPE=IMS",
                "SHARE LEVEL=0               GSGNAME=**NULL**     USID=0000000001",
                "AUTHORIZED USID=0000000000  RECEIVE USID=0000000000 HARD USID=0000000000",
                "RECEIVE NEEDED USID=0000000000",
                "DBRCVGRP=**NULL**",
                "'FLAGS:                             COUNTERS:'",
                "BACKOUT NEEDED        =OFF         RECOVERY NEEDED COUNT   =0",
                "READ ONLY             =OFF         IMAGE COPY NEEDED COUNT =0",
                "PROHIBIT AUTHORIZATION=OFF         AUTHORIZED SUBSYSTEMS   =0",
                "RECOVERABLE           =YES         HELD AUTHORIZATION STATE=0",
                "EEQE COUNT              =0",
                "TRACKING SUSPENDED    =NO          RECEIVE REQUIRED COUNT  =0",
                "OFR REQUIRED          =NO",
                "REORG INTENT          =NO",
                "QUIESCE IN PROGRESS   =NO",
                "QUIESCE HELD          =NO",
                "'--------------------------------------------------------------------------'",
                "DB",
                "DBD=CUSTACCS                                     DMB#=3       TYPE=IMS",
                "SHARE LEVEL=0               GSGNAME=**NULL**     USID=0000000001",
                "AUTHORIZED USID=0000000000  RECEIVE USID=0000000000 HARD USID=0000000000",
                "RECEIVE NEEDED USID=0000000000",
                "DBRCVGRP=**NULL**",
                "'FLAGS:                             COUNTERS:'",
                "BACKOUT NEEDED        =OFF         RECOVERY NEEDED COUNT   =0",
                "READ ONLY             =OFF         IMAGE COPY NEEDED COUNT =0",
                "PROHIBIT AUTHORIZATION=OFF         AUTHORIZED SUBSYSTEMS   =0",
                "RECOVERABLE           =YES         HELD AUTHORIZATION STATE=0",
                "EEQE COUNT              =0",
                "TRACKING SUSPENDED    =NO          RECEIVE REQUIRED COUNT  =0",
                "OFR REQUIRED          =NO",
                "REORG INTENT          =NO",
                "QUIESCE IN PROGRESS   =NO",
                "QUIESCE HELD          =NO"
            ],
            "msg": "Success"
        },

        {
            "command": "LIST.DBDS DBD(CUSTOMER)",
            "data": [
                "LIST.DBDS DBD(CUSTOMER)",
                "'--------------------------------------------------------------------------'",
                "DBDS",
                "DSN=IMSBANK.IMS1.CUSTOMER.DB                                  TYPE=IMS",
                "DBD=CUSTOMER  DDN=CUSTOMER DSID=001 DBORG=HDAM   DSORG=OSAM",
                "CAGRP=**NULL**  GENMAX=2     IC AVAIL=0     IC USED=0     DSSN=00000000",
                "NOREUSE         RECOVPD=0",
                "DEFLTJCL=**NULL**  ICJCL=ICJCL     OICJCL=OICJCL    RECOVJCL=RECOVJCL",
                "RECVJCL=ICRCVJCL",
                "'FLAGS:                             COUNTERS:'",
                "IC NEEDED      =OFF",
                "IC RECOMMENDED =ON",
                "RECOV NEEDED   =OFF",
                "RECEIVE NEEDED =OFF                EEQE COUNT              =0",
                "DSP0180I  NUMBER OF RECORDS LISTED IS        1",
                "DSP0203I  COMMAND COMPLETED WITH CONDITION CODE 00",
                "DSP0220I  COMMAND COMPLETION TIME 20.139 19:48:10.874690",
                "DSP0211I  COMMAND PROCESSING COMPLETE",
                "DSP0211I  HIGHEST CONDITION CODE = 00",
                "DSP0058I  RML COMMAND COMPLETED"
            ],
            "msg": "Success"
        }
    ]
}
```

The final option is similar to the second option, but the data will be parsed so that each individual field in the output is mapped to its corresponding value where applicable.
```
{
    "changed": "true"
    "failed": "false"
    "dbrc_output": [{
            "COMMAND": "LIST.RECON STATUS",
            "DATA": [
                {
                    "RECON": "",
                    "RECOVERY CONTROL "DATA" SET, IMS V15R1": "", 
                    "DMB#": "5",
                    "INIT TOKEN": "20139F1535085F",
                    "FORCER": ""
                    "LOG DSN CHECK": "CHECK44",
                    "STARTNEW": "NO",
                    "TAPE UNIT": "",
                    "DASD UNIT": "SYSALLDA TRACEOFF",
                    "SSID": "IMS1",
                    "LIST DLOG": "NO",
                    "CA/IC/LOG "DATA" SETS CATALOGED": "YES",
                    "MINIMUM VERSION": "13.1",
                    "CROSS DBRC SERVICE LEVEL ID": "00002",
                    "REORG NUMBER VERIFICATION": "NO",
                    "LOG RETENTION PERIOD": "00.001 00:00:00.0",
                    "COMMAND AUTH": "NONE",
                    "HLQ": "**NULL**",
                    "RCNQUAL": "**NULL**",
                    "CATALOG": "**NULL**",
                    "ACCESS": "SERIAL",
                    "LIST": "STATIC",
                    "SIZALERT DSNUM": "15",
                    "VOLNUM": "16",
                    "PERCENT": "95",
                    "LOGALERT DSNUM": "3",
                    "VOLNUM": "16",
                    "TIME STAMP INFORMATION" : {
                        "TIMEZIN": "%SYS"
                    },
                    "OUTPUT FORMAT": {
                        "DEFAULT": "LOCORG NONE   PUNC YY",
                        "CURRENT": "LOCORG NONE   PUNC YY",
                    }
                    "IMSPLEX": "** NONE **",
                    "GROUP ID": "** NONE **",
                    "DD INFO": [
                        {
                            "DDNAME": "RECON1",
                            "STATUS": "COPY1",
                            ""DATA" SET NAME": "IMSBANK.IMS1.RECON1"
                        },
                        {
                            "DDNAME": "RECON2",
                            "STATUS": "COPY2",
                            ""DATA" SET NAME": "IMSBANK.IMS1.RECON2"
                        },
                        {
                            "DDNAME": "RECON3",
                            "STATUS": "SPARE",
                            ""DATA" SET NAME": "IMSBANK.IMS1.RECON3"
                        }
                    ]
                    "NUMBER OF REGISTERED "DATA"BASES": "5",
                    "DSP0180I  NUMBER OF RECORDS LISTED IS        1": "",
                    "DSP0203I  COMMAND COMPLETED WITH CONDITION CODE 00": "",
                    "DSP0220I  COMMAND COMPLETION TIME 20.139 19:48:09.753357": "",
                    "DSP0211I  COMMAND PROCESSING COMPLETE": "",
                    "DSP0211I  HIGHEST CONDITION CODE": "00",
                    "DSP0058I  RML COMMAND COMPLETED": ""
                }
            ],
            "msg": "Success"
        },

        {
            "COMMAND": "LIST.DB ALL",
            "DATA": [
                {
                    "DB": "",
                    "DBD": "ACCOUNT",
                    "DMB#": "2",
                    "TYPE": "IMS",
                    "SHARE LEVEL": "0"
                    "GSGNAME": "**NULL**"
                    "USID": "0000000001",
                    "AUTHORIZED USID": "0000000000"
                    "RECEIVE USID": "0000000000"
                    "HARD USID": "0000000000",
                    "RECEIVE NEEDED USID": "0000000000",
                    "DBRCVGRP": "**NULL**",
                    "FLAGS": {
                        "BACKOUT NEEDED": "OFF",
                        "READ ONLY": "OFF",
                        "PROHIBIT AUTHORIZATION": "OFF",
                        "RECOVERABLE": "YES",
                        "EEQE COUNT": "0",
                        "TRACKING SUSPENDED": "NO",
                        "OFR REQUIRED": "NO",
                        "REORG INTENT": "NO",
                        "QUIESCE IN PROGRESS": "NO",
                        "QUIESCE HELD": "NO",
                    },
                    "COUNTERS": {
                        "RECOVERY NEEDED COUNT": "0",
                        "IMAGE COPY NEEDED COUNT": "0",
                        "AUTHORIZED SUBSYSTEMS": "0",
                        "HELD AUTHORIZATION STATE": "0",
                        "RECEIVE REQUIRED COUNT": "0",
                    }
                },
                {
                    "DB": "",
                    "DBD": "CUSTACCS",
                    "DMB#": "3",
                    "TYPE": "IMS",
                    "SHARE LEVEL": "0"
                    "GSGNAME": "**NULL**"
                    "USID": "0000000001",
                    "AUTHORIZED USID": "0000000000"
                    "RECEIVE USID": "0000000000"
                    "HARD USID": "0000000000",
                    "RECEIVE NEEDED USID": "0000000000",
                    "DBRCVGRP": "**NULL**",
                    "FLAGS": {
                        "BACKOUT NEEDED": "OFF",
                        "READ ONLY": "OFF",
                        "PROHIBIT AUTHORIZATION": "OFF",
                        "RECOVERABLE": "YES",
                        "TRACKING SUSPENDED": "NO",
                        "OFR REQUIRED": "NO",
                        "REORG INTENT": "NO",
                        "QUIESCE IN PROGRESS": "NO",
                        "QUIESCE HELD": "NO",
                    },
                    "COUNTERS": {
                        "RECOVERY NEEDED COUNT": "0",
                        "IMAGE COPY NEEDED COUNT": "0",
                        "AUTHORIZED SUBSYSTEMS": "0",
                        "HELD AUTHORIZATION STATE": "0",
                        "EEQE COUNT": "0",
                        "RECEIVE REQUIRED COUNT": "0",
                    }
                }
            ],
            "msg": "Success"
        },

        {
            "COMMAND": "LIST.DBDS DBD(CUSTOMER)",
            "DATA": [
                {
                    "DBDS": "",
                    "DSN": "IMSBANK.IMS1.CUSTOMER.DB",
                    "TYPE": "IMS",
                    "DBD": "CUSTOMER",
                    "DDN": "CUSTOMER",
                    "DSID": "001",
                    "DBORG": "HDAM",
                    "DSORG": "OSAM",
                    "CAGRP": "**NULL**",
                    "GENMAX": "2",
                    "IC AVAIL": "0",
                    "IC USED": "0",
                    "DSSN": "00000000",
                    "NOREUSE": "",
                    "RECOVPD": "0",
                    "DEFLTJCL": "**NULL**",
                    "ICJCL": "ICJCL",
                    "OICJCL": "OICJCL",
                    "RECOVJCL": "RECOVJCL",
                    "RECVJCL": "ICRCVJCL",
                    "FLAGS": {
                        "IC NEEDED": "OFF",
                        "IC RECOMMENDED": "ON",
                        "RECOV NEEDED": "OFF",
                        "RECEIVE NEEDED": "OFF"
                    }
                    "COUNTERS": {
                        "EEQE COUNT": "0",
                    }                            
                    "DSP0180I  NUMBER OF RECORDS LISTED IS        1": "",
                    "DSP0203I  COMMAND COMPLETED WITH CONDITION CODE 00": "",
                    "DSP0220I  COMMAND COMPLETION TIME 20.139 19:48:10.874690": "",
                    "DSP0211I  COMMAND PROCESSING COMPLETE": "",
                    "DSP0211I  HIGHEST CONDITION CODE": "00",
                    "DSP0058I  RML COMMAND COMPLETED": ""
                }

            ],
            "msg": "Success"
        }
    ]
}
```