
:github_url: https://github.com/ansible-collections/ibm_zos_core/blob/dev/plugins/modules/ims_ddl.py

.. _ims_ddl_module:


ims_ddl -- Submits Data Definition Language (DDL) SQL statements.
=================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The IMS Data Definition utility (DFS3ID00) utility writes the metadata for your application programs (PSBs) and databases definitions to the IMS Catalog records and the runtime blocks to the staging directory dataset.





Parameters
----------


online
  Indicates if this utility is to be run in a BMP region.

  If online is true, its BMP enabled.

  online is false is DLI that is not supported currently.

  | **required**: False
  | **type**: bool
  | **default**: True


ims_id
  The identifier of the IMS system on which the job is to be run.

  Required if online is true.

  | **required**: False
  | **type**: str


reslib
  Points to an authorized library that contains the IMS SVC modules.

  | **required**: False
  | **type**: list
  | **elements**: str


proclib
  Defines the IMS.PROCLIB data set that contains the DFSDFxxx member. The DFSDFxxx member defines various attributes of the IMS catalog that are required by the utility.

  | **required**: True
  | **type**: list
  | **elements**: str


steplib
  Points to IMS.SDFSRESL, which contains the IMS nucleus and required IMS modules.

  The steplib parameter can also be specified in the target inventory's environment\_vars.

  The steplib input parameter to the module will take precedence over the value specified in the environment\_vars.

  | **required**: False
  | **type**: list
  | **elements**: str


sql_input
  Defines the SQL DDL statements to be run.

  Can specify the DDL statements in a dataset or dataset member.

  The following concatenations are not supported - Cannot mix FB and VB data sets. - Cannot have concatenated FB data sets with different LRECLs.

  | **required**: True
  | **type**: str


verbose
  Specifies that the DFS3ID00 utility will print full text of the DDL statements in the job log.

  If VERBOSE control option is not specified, then utility will only print full text of failing DDL statement.

  | **required**: False
  | **type**: bool


auto_commit
  Specifies that the DFS3ID00 utility will perform auto Commit if no COMMIT DDL statement is provided by the user.

  If user does not specify AUTOCOMMIT control option or COMMIT DDL statement, then utility will perform auto ROLLBACK DDL.

  | **required**: False
  | **type**: bool


simulate
  Specifies that the DFS3ID00 utility will perform simulation of DDL statements which includes parser validations, commit level validations, block builder validations, and DROP DDL cross-reference validations.

  | **required**: False
  | **type**: bool


dynamic_programview
  Directly maps to DYNAMICPROGRAMVIEW=(CREATEYES | CREATENO) of IMS Data Definition utility utility.

  Specifies that the DFS3ID00 utility will automatically import all the input CREATE PROGRAMVIEWs.

  If CREATEYES is specified, then PDIR will be created with the DOPT flag ON.

  If CREATENO is specified, then PDIR will not be created.

  | **required**: False
  | **type**: bool




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Example of DDL statements are in a dataset
     ims_ddl:
       online: True
       ims_id: IMS1
       reslib:
         - SOME.IMS.SDFSRESL
       steplib:
         - SOME.IMS.SDFSRESL
       proclib:
         - SOME.IMS.PROCLIB
       sql_input: SOME.IMS.SQL
   - name: Example of DDL statements in which VERBOSE and AUTOCOMMIT control options are specified
     ims_ddl:
       online: True
       ims_id: IMS1
       reslib:
         - SOME.IMS.SDFSRESL
       steplib:
         - SOME.IMS.SDFSRESL
       proclib:
         - SOME.IMS.PROCLIB
       sql_input: SOME.IMS.SQL
       verbose: true
       auto_commit: true

   - name: Example of DDL statements in which SIMULATE control options is specified
     ims_ddl:
       online: True
       ims_id: IMS1
       reslib:
         - SOME.IMS.SDFSRESL
       steplib:
         - SOME.IMS.SDFSRESL
       proclib:
         - SOME.IMS.PROCLIB
       sql_input: SOME.IMS.SQL
       simulate: true

   - name: Example of DDL statements in which DYNAMIC_PROGRAMVIEW control option is specified
     ims_ddl:
       online: True
       ims_id: IMS1
       reslib:
         - SOME.IMS.SDFSRESL
       steplib:
         - SOME.IMS.SDFSRESL
       proclib:
         - SOME.IMS.PROCLIB
       sql_input: SOME.IMS.SQL
       dynamic_programview: true





Notes
-----

.. note::
   The \ :emphasis:`steplib`\  parameter can also be specified in the target inventory's environment\_vars.

   The \ :emphasis:`steplib`\  input parameter to the module will take precedence over the value specified in the environment\_vars.

   If only the \ :emphasis:`steplib`\  parameter is specified, then only the \ :emphasis:`steplib`\  concatenation will be used to resolve the IMS RESLIB data set.

   Specifying only \ :emphasis:`reslib`\  without \ :emphasis:`steplib`\  is not supported.

   Currently ddl error messages are returned within the content block of the module response.

   Currently this module only supports running the DDL utility in a BMP region (online is true).







Return Values
-------------


content
  The standard output returned running the Data Definition module.

  | **returned**: sometimes
  | **type**: str
  | **sample**: entire block

rc
  The return code from the Data Definition utility.

  | **returned**: sometimes
  | **type**: str
  | **sample**: 1

changed
  Indicates if any changes were made during module execution.

  True is always returned unless a module or failure has occurred.

  | **returned**: always
  | **type**: bool

stderr
  The standard error output returned from running the Data Definition utility.

  | **returned**: sometimes
  | **type**: str

msg
  Messages returned from the Data Definition Ansible module.

  | **returned**: sometimes
  | **type**: str

