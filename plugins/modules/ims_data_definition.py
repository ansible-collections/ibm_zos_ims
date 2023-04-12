#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = r'''
---

module: ims_data_definition
short_description: Submits Data Definition Language (DDL) SQL statements.
version_added: "1.1.0"
description:
  - The IMS Data Definition utility (DFS3ID00) utility writes the metadata for your application programs (PSBs) and databases
    definitions to the IMS Catalog records and the runtime blocks to the staging directory dataset.

# Prerequisites
 # - IMS managed ACBs must be enabled

author:
  - Dipti Gandhi (@ddgandhi)
options:
  online:
    description:
      - Indicates if this utility is to be run in a BMP region.
    type: bool
    required: true
    default: true
  ims_id:
    description:
      - The identifier of the IMS system on which the job is to be run.
      - Required if online is true
    type: str
    required: false
  irlm_id:
    description:
      - The IRLM ID if IRLM is enabled. Cannot be specified when online is true.
    type: str
    required: false
  reslib:
    description:
      - Points to an authorized library that contains the IMS SVC modules.
    type: list
    required: false
    elements: str
  proclib:
    description:
      - Defines the IMS.PROCLIB data set that contains the DFSDFxxx member. The DFSDFxxx member
        defines various attributes of the IMS catalog that are required by the utility.
    type: list
    required: true
    elements: str
  steplib:
    description:
      - Points to IMS.SDFSRESL, which contains the IMS nucleus and required IMS modules.
      - The steplib parameter can also be specified in the target inventory's environment_vars.
      - The steplib input parameter to the module will take precedence over the value specified in the environment_vars.
    type: list
    required: False
    elements: str
  # sysabend:
  #   description:
  #     - Defines the dump data set. This defaults to = \*
  #   type: str
  #   required: false
  sql_input:
    description:
      - Defines the SQL DDL statements to be run.
      - Can specify the DDL statements inline or in a data set.
      - Any data sets concatenated with inline must be FB LRECL 80.
      - The following concatenations are not supported:
        - Cannot mix FB and VB data sets.
        - Cannot have concatenated FB data sets with different LRECLs.
        - Cannot have VB data sets concatenated with inline.
    type: list
    required: true
    elements: str

  control_statements:
    description:
      - The control statement parameters.
    type: dict
    required: false
    suboptions:
      verbose:
        description:
          - Specifies that the DFS3ID00 utility will print full text of the DDL statements in the job log.
          - If VERBOSE control option is not specified, then utility will only print full text of failing DDL statement.
        type: bool
        required: false
      auto_commit:
        description:
          - Specifies that the DFS3ID00 utility will perform auto Commit if no COMMIT DDL statement is provided by the user.
          - If user does not specify AUTOCOMMIT control option or COMMIT DDL statement, then utility will perform auto ROLLBACK DDL.
        type: bool
        required: false
      simulate:
        description:
          - Specifies that the DFS3ID00 utility will perform simulation of DDL statements which includes parser validations,
            commit level validations, block builder validations, and DROP DDL cross-reference validations.
        type: bool
        required: false
      create_program_view:
        description:
          - Specifies that the DFS3ID00 utility will automatically Import all the input CREATE PROGRAMVIEWs.
          - If CREATEYES is specified, then PDIR will be created with the DOPT flag ON.
          - If CREATENO is specified, then PDIR will not be created.
        type: bool
        required: false
        default: false

notes:
  - The I(steplib) parameter can also be specified in the target inventory's environment_vars.
  - The I(steplib) input parameter to the module will take precedence over the value specified in the environment_vars.
  - If only the I(steplib) parameter is specified, then only the I(steplib) concatenation will be used to resolve the IMS RESLIB data set.
  - Specifying only I(reslib) without I(steplib) is not supported.
'''

EXAMPLES = '''
- name: Example of DDL statements are specified inline
  ims_data_definition:
    online_batch: True
    ims_id: IMS1
    reslib:
      - SOME.IMS.SDFSRESL
    steplib:
      - SOME.IMS.SDFSRESL
    proclib:
      - SOME.IMS.PROCLIB
    ims_sql:
      - DROP PROGRAMVIEW DYNPSB;
      - COMMIT DDL;

- name: Example of DDL statements are in a dataset
  ims_data_definition:
    online_batch: True
    ims_id: IMS1
    reslib:
      - SOME.IMS.SDFSRESL
    steplib:
      - SOME.IMS.SDFSRESL
    proclib:
      - SOME.IMS.PROCLIB
    ims_sql:
      - USER1.DDL(DEDBJN21)
      - USER.DDL(DEDBJN41)

- name: Example of DDL statements in which VERBOSE and AUTOCOMMIT control options are specified
  ims_data_definition:
    online_batch: True
    ims_id: IMS1
    reslib:
      - SOME.IMS.SDFSRESL
    steplib:
      - SOME.IMS.SDFSRESL
    proclib:
      - SOME.IMS.PROCLIB
    ims_sql:
    	- USER1.DDL(TESTDB01)
      - USER.DDL(TESTPSB1)
    verbose: true
    auto_commit: true

- name: Example of DDL statements in which SIMULATE control options is specified
  ims_data_definition:
    online_batch: True
    ims_id: IMS1
    reslib:
      - SOME.IMS.SDFSRESL
    steplib:
      - SOME.IMS.SDFSRESL
    proclib:
      - SOME.IMS.PROCLIB
    ims_sql:
      - USER1.DDL(TESTDB02)
      - USER.DDL(TESTPSB2)
    simulate: true

- name: Example of Data sets concatenated with inline on IMSSQL DD
  ims_data_definition:
    online_batch: True
    ims_id: IMS1
    reslib:
      - SOME.IMS.SDFSRESL
    steplib:
      - SOME.IMS.SDFSRESL
    proclib:
      - SOME.IMS.PROCLIB
    ims_sql:
      - CREATE DATABASE DEMODB1;
      - CREATE TABLE T1(C1 INT PRIMARY KEY);
      - USER.DDL(TESTDB02)
      - USER.DDL(TESTDB03)
      - DROP PROGRAMVIEW DEMOPSB1 IF EXISTS;
      - CREATE PROGRAMVIEW DEMOPSB1
      - (CREATE SCHEMA S1 USING DEMODB1 AS S1
      - (CREATE SENSEGVIEW T1)
      - ) LANGASSEM;
    auto_commit: true


'''

RETURN = '''
content:
  description: The standard output returned running the Data Definition module.
  type: str
  returned: sometimes
  sample: DFS4434I INSTANCE 2020200562326 OF DBD AUTODB   WAS ADDED TO A NEWLY CREATED RECORD IN THE IMS CATALOG.
rc:
  description: The return code from the Data Definition utility.
  type: str
  returned: sometimes
  sample: '1'
stderr:
  description: The standard error output returned from running the Data Definition utility.
  type: str
  returned: sometimes
msg:
  description: Messages returned from the Data Definition module.
  type: str
  returned: sometimes
  sample: You cannot define directory data sets, the bootstrap data set, or directory staging data sets with MANAGEDACBS=STAGE or MANAGEDACBS=UPDATE
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.catalog import catalog  # pylint: disable=import-error
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.catalog_parser import catalog_parser  # pylint: disable=import-error

# module = None

def run_module():
    module_args = dict(
        online=dict(type="bool", required=True, default=True),
        ims_id=dict(type="str", required=False),
        irlm_id=dict(type="str", required=False),
        reslib=dict(type="list", elements="str", required=False),
        proclib=dict(type="list", elements="str", required=True),
        steplib=dict(type="list", elements="str", required=False),
        sql_input=dict(type="list", elements="str", required=True),
        # sysabend=dict(type="str", required=False),
        control_statements=dict(type="dict", required=False)
    )

    global module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {}
    result["changed"] = False

    parsed_args = catalog_parser(module, module.params, result).validate_populate_input()
    response = catalog(module, result, parsed_args).execute_catalog_populate()

    # if module.params['mode'] != "READ":
    #     result["changed"] = True

    module.exit_json(**response)


def main():
    run_module()


if __name__ == '__main__':
    main()
