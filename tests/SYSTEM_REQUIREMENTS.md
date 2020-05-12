# z/OS System Requirements for Ansible Module Testing

This document outlines system/environment prerequisites needed to run and develop test cases for IMS Ansible modules.

- [IMS DBD Gen](#ims_dbd_gen)
- [IMS PSB Gen](#ims_psb_gen)
- [IMS Command](#ims_command)

## ims_dbd_gen

* **"IMSTESTU.ANSIBLE.DBD.SRC"** is a PDS containing IMS DBD source to be compiled.

* **"IMSBLD.I15RTSMM.SDFSMAC"** and **"SYS1.MACLIB"** serve as a macro library used to compile DBD source.

* **"IMSTESTU.ANSI.DBDLIB"** is the target for generated DBD members 

* **"IMSTESTU.ANS.SEQ"** is a sequential data set containing IMS DBD source to be compiled. 

* **'/tmp/dbdgen02'** is a USS binary of IMS DBD source to be compiled. 

## ims_psb_gen

* **"IMSTESTU.ANSIBLE.PSB.SRC"** is a PDS containing IMS PSB source to be compiled.

* ***TODO*** -- there will be a library of macros to compile the PSB

* **"IMSTESTU.ANSIBLE.PSBLIB"** is the target for generated PSB members.

## ims_command

* DRD must be enabled on the target system.
* IMS should be up.