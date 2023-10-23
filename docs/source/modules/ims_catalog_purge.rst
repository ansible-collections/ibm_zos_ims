.. _ims_catalog_purge_module:


ims_catalog_purge -- Purge records from the IMS Catalog
=======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The IMS Catalog Purge  utility DFS3PU10 removes the segments that represent a DBD or PSB instance, all instances of a DBD version, or an entire DBD or PSB record from the IMS catalog. You can also analyze the catalog and generate delete statements for ACBs eligible for deletion, as well as update the ACB retention criteria.






Parameters
----------

  mode (True, str, None)
    Determines which mode the utility runs in. ANALYSIS mode generates delete statements based on the retention criteria and places them in the SYSUT1 data set. PURGE mode executes delete statements in the SYSUT1 data set. BOTH mode performs ANALYSIS and PURGE mode consecutively.


  online_batch (False, bool, False)
    Indicates if this utility is to be run in a BMP region.


  ims_id (False, str, None)
    The identifier of the IMS system on which the job is to be run.

    Required if online\_batch is true.


  dbrc (False, bool, None)
    Indicates if the IMS Database Recovery Control facility is enabled.


  irlm_id (False, str, None)
    The IRLM ID if IRLM is enabled. Cannot be specified when online\_batch is true.


  reslib (False, list, None)
    Points to an authorized library that contains the IMS SVC modules.


  buffer_pool_param_dataset (False, str, None)
    Defines the buffer pool parameters data set. This option is required if you are running the utility as a DLI.


  primary_log_dataset (True, dict, None)
    Defines the primary IMS log data set. This option is required if you are running the utility as a DLI.


    dataset_name (True, str, None)
      Describes the name of the data set.


    disposition (False, str, None)
      The status of the data set.


    record_format (False, str, None)
      The record format.


    record_length (False, int, None)
      The logical record length in bytes.


    block_size (False, int, None)
      The block size.


    primary (False, int, None)
      The amount of primary space to allocate for the data set.


    primary_unit (False, str, None)
      The unit of size to use when specifying primary space.


    secondary (False, int, None)
      The amount of secondary space to allocate for the data set.


    secondary_unit (False, str, None)
      The unit of size to use when specifying secondary space.


    normal_disposition (False, str, None)
      Data set action after normal termination.


    abnormal_disposition (False, str, None)
      Data set action after abnormal termination.


    type (False, str, None)
      The type of data set.


    volumes (False, list, None)
      A list of volume serials. When providing multiple volumes, processing will begin with the first volume in the provided list. Offline volumes are not considered.


    storage_class (False, str, None)
      The storage class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    management_class (False, str, None)
      The management class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    data_class (False, str, None)
      The data class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.



  psb_lib (True, list, None)
    Defines the IMS.PSBLIB data set.


  dbd_lib (True, list, None)
    Defines the IMS.DBDLIB data sets.


  proclib (True, list, None)
    Defines the IMS.PROCLIB data set that contains the DFSDFxxx member. The DFSDFxxx member defines various attributes of the IMS catalog that are required by the utility.


  steplib (False, list, None)
    Points to IMS.SDFSRESL, which contains the IMS nucleus and required IMS modules.

    The steplib parameter can also be specified in the target inventory's environment\_vars.

    The steplib input parameter to the module will take precedence over the value specified in the environment\_vars.


  delete_dbd_by_version (False, list, None)
    Delete DBD instances based on the specified name and version. If ANALYSIS mode is specified, it will generate DELETE DBD statements in the SYSUT1 data set along with any other delete statements based off the retention criteria. If PURGE or BOTH mode is specified, it will write the delete statements to the SYSUT1 data set and then execute them.


    member_name (True, str, None)
      The 8 character name of the DBD that you are deleting a version from.


    version_number (True, int, None)
      The version number of the DBD that you are deleting. The value must match the version number that is specified on the DBVER keyword in the DBD generation statement of the version that you are deleting.



  update_retention_criteria (False, list, None)
    Use this statement to set the retention criteria for DBD or PSB records in the catalog database. You can submit any number of update statements. You cannot specify this option if PURGE mode is selected. If used with any other mode options, it will update the retention criteria first.


    resource (True, str, None)
      Specifies whether a DBD or PSB should be updated.


    member_name (True, str, None)
      The 8 character IMS name of the DBD or PSB resource. Wildcards are supported.


    instances (True, int, None)
      The number of instances of a DBD or PSB that must be retained in the DBD or PSB record.


    days (False, int, None)
      The number of days that an instance of a DBD or PSB must be retained before it can be purged.



  delete (False, list, None)
    Specifies a DBD or PSB instance or an entire DBD or PSB record to delete from the IMS catalog database.

    This option must be used with PURGE mode and overrides any retention criteria, hence you can remove any DBD or PSB that would not otherwise be eligible for deletion.


    resource (True, str, None)
      Specify whether you want to delete a DBD or PSB.


    member_name (True, str, None)
      The 8 character IMS name of the DBD or PSB resource. Wildcards are supported.


    time_stamp (True, int, None)
      The ACB timestamp that identifies the specific DBD or PSB instance to purge.



  managed_acbs (False, bool, None)
    Specifies whether deleting DBD and PSB instances from the IMS catalog causes the corresponding DBD and PSB instances in the IMS directory to be deleted. If 'analysis\_mode' is true, the DBD and PSB instances will not be deleted from the IMS directory.


  resource_chkp_freq (False, int, None)
    Specifies the number of resource instances to be deleted or updated between checkpoints. Can be a 1 to 8 digit numeric value between 1 to 99999999. The default value is 200.


  sysut1 (False, dict, None)
    The data set where delete statements are written to. Written either by the purge utility when specifying ANALYSIS or BOTH mode, or by the user when specifying PURGE mode.


    dataset_name (True, str, None)
      Describes the name of the data set.


    disposition (False, str, None)
      The status of the data set.


    block_size (False, int, None)
      The block size.


    primary (False, int, None)
      The amount of primary space to allocate for the data set.


    primary_unit (False, str, None)
      The unit of size to use when specifying primary space.


    secondary (False, int, None)
      The amount of secondary space to allocate for the data set.


    secondary_unit (False, str, None)
      The unit of size to use when specifying secondary space.


    normal_disposition (False, str, None)
      Data set action after normal termination.


    abnormal_disposition (False, str, None)
      Data set action after abnormal termination.


    type (False, str, None)
      The type of the data set.


    volumes (False, list, None)
      A list of volume serials. When providing multiple volumes, processing will begin with the first volume in the provided list. Offline volumes are not considered.


    storage_class (False, str, None)
      The storage class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    management_class (False, str, None)
      The management class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    data_class (False, str, None)
      The data class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.






Notes
-----

.. note::
   - The \ :emphasis:`steplib`\  parameter can also be specified in the target inventory's environment\_vars.
   - The \ :emphasis:`steplib`\  input parameter to the module will take precedence over the value specified in the environment\_vars.
   - If only the \ :emphasis:`steplib`\  parameter is specified, then only the \ :emphasis:`steplib`\  concatenation will be used to resolve the IMS RESLIB data set.
   - Specifying only \ :emphasis:`reslib`\  without \ :emphasis:`steplib`\  is not supported.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Purge the IMS Catalog of DBDs beginning with 'DB'
      ims_catalog_purge:
        reslib:
          - SOME.IMS.SDFSRESL
        steplib:
          - SOME.IMS.SDFSRESL
        proclib:
          - SOME.IMS.PROCLIB
        dbd_lib:
          - SOME.IMS.DBDLIB
        psb_lib:
          - SOME.IMS.PSBLIB
        buffer_pool_param_dataset: "SOME.IMS1.PROCLIB(DFSVSMHP)"
        primary_log_dataset:
          dataset_name: SOME.IMS.LOG1
        mode: PURGE
        delete:
          - resource: DBD
            member_name: 'AUTODB'
            time_stamp: 500

    - name: Purge the IMS Catalog and the IMS Directory of DBDs beginning with 'DB'
      ims_catalog_purge:
        reslib:
          - SOME.IMS.SDFSRESL
        steplib:
          - SOME.IMS.SDFSRESL
        proclib:
          - SOME.IMS.PROCLIB
        dbd_lib:
          - SOME.IMS.DBDLIB
        psb_lib:
          - SOME.IMS.PSBLIB
        buffer_pool_param_dataset: "SOME.IMS1.PROCLIB(DFSVSMHP)"
        primary_log_dataset:
          dataset_name: SOME.IMS.LOG1
        mode: PURGE
        delete:
          - resource: DBD
            member_name: AUTODB
            time_stamp: 500
        managed_acbs: true

    - name: Analyze the IMS Catalog and generate delete statements for resources eligible for deletion
      ims_catalog_purge:
        reslib:
          - SOME.IMS.SDFSRESL
        steplib:
          - SOME.IMS.SDFSRESL
        proclib:
          - SOME.IMS.PROCLIB
        dbd_lib:
          - SOME.IMS.DBDLIB
        psb_lib:
          - SOME.IMS.PSBLIB
        buffer_pool_param_dataset: "SOME.IMS1.PROCLIB(DFSVSMHP)"
        primary_log_dataset:
          dataset_name: SOME.IMS.LOG1
        mode: ANALYSIS

    - name: Update resource retention criteria for resources in the IMS Catalog while running as BMP
      ims_catalog_purge:
        online_batch: True
        ims_id: IMS1
        reslib:
          - SOME.IMS.SDFSRESL
        steplib:
          - SOME.IMS.SDFSRESL
        proclib:
          - SOME.IMS.PROCLIB
        dbd_lib:
          - SOME.IMS.DBDLIB
        psb_lib:
          - SOME.IMS.PSBLIB
        buffer_pool_param_dataset: "SOME.IMS1.PROCLIB(DFSVSMHP)"
        primary_log_dataset:
          dataset_name: SOME.IMS.LOG1
        mode: ANALYSIS
        update_retention_criteria:
          - resource: DBD
            member_name: AUTODB
            instances: 0
            days: 0
          - resource: PSB
            member_name: DBF000
            instances: 0
            days: 0



Return Values
-------------

content (always, str, DFS4810I ALL OF THE MEMBER INSTANCES THAT ARE REFERENCED IN THE SYSUT1 DATA SET WERE DELETED FROM THE IMS CATALOG.)
  The standard output returned running the IMS Catalog Purge utility.


rc (sometimes, str, 0)
  The return code from the IMS Catalog Purge utility.


stderr (sometimes, str, 12.27.08 STC00143  +DFS671I OMVSADM8.STEP1. - FOR THIS EXECUTION, DBRC IS SET TO NO     IMS1)
  The standard error output returned from running the IMS Catalog Purge utility.


msg (sometimes, str, You must specify a buffer pool parameter data set when running as DLI.)
  Messages returned from the IMS Catalog Purge module.





Status
------





Authors
~~~~~~~

- Jerry Li (@th365thli)

