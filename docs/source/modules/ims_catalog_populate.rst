.. _ims_catalog_populate_module:


ims_catalog_populate -- Add records to the  IMS Catalog
=======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The IMS Catalog Populate utility DFS3PU00 loads, inserts, or updates DBD and PSB instances into the database data sets of the IMS catalog from ACB library data sets.






Parameters
----------

  mode (True, str, None)
    Indicates the mode in which the Catalog Populate utility must be run.


  online_batch (False, bool, False)
    Indicates if this utility is to be run in a BMP region.


  ims_id (False, str, None)
    The identifier of the IMS system on which the job is to be run.

    Required if online\_batch is true


  dbrc (False, bool, None)
    Indicates if the IMS Database Recovery Control facility is enabled.


  irlm_id (False, str, None)
    The IRLM ID if IRLM is enabled. Cannot be specified when online\_batch is true.


  modstat (False, str, None)
    Describes the IMS MODSTAT data set.


  reslib (False, list, None)
    Points to an authorized library that contains the IMS SVC modules.


  buffer_pool_param_dataset (False, str, None)
    Defines the buffer pool parameters data set. This option is required if you are running the utility as a DLI.


  dfsdf_member (False, str, None)
    The DFSDFxxx member in the IMS.PROCLIB data set where the CATALOG section is defined. For example, dfsdf\_member is "CAT" specifies the DFSDFCAT member of the PROCLIB data set.


  primary_log_dataset (False, dict, None)
    Defines the primary IMS log data set. This is required if dbrc is set to true or if mode 'UPDATE' is selected.


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


    volumes (False, list, None)
      A list of volume serials. When providing multiple volumes, processing will begin with the first volume in the provided list. Offline volumes are not considered.


    type (False, str, None)
      The type of data set.


    storage_class (False, str, None)
      The storage class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    management_class (False, str, None)
      The management class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    data_class (False, str, None)
      The data class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.



  secondary_log_dataset (False, dict, None)
    Defines the secondary IMS log data set.


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
      Data set action after abnormal termination


    volumes (False, list, None)
      A list of volume serials. When providing multiple volumes, processing will begin with the first volume in the provided list. Offline volumes are not considered.


    type (False, str, None)
      The type of data set.


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


  check_timestamp (False, bool, True)
    Determines if the utility should check timestamps of ACB members with duplicate names.

    If true, the utility will check if the ACB generation timestamp is different from the previously processed ACB member with the same name.

    If the timestamp is different, it will use the ACB with the duplicate name. If not, it will ignore the ACB with the duplicate name.


  acb_lib (True, list, None)
    Defines an ACB library data set that contains the ACB members that are used to populate the IMS catalog.


  bootstrap_dataset (False, dict, None)
    Optionally defines the IMS directory bootstrap data set.


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
      Data set action after abnormal termination


    volumes (False, list, None)
      A list of volume serials. When providing multiple volumes, processing will begin with the first volume in the provided list. Offline volumes are not considered.


    storage_class (False, str, None)
      The storage class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    management_class (False, str, None)
      The management class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    data_class (False, str, None)
      The data class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.



  directory_datasets (False, list, None)
    Optionally defines the IMS directory data sets that are used to store the ACBs.

    If this is omitted, the utility dynamically deletes any preexisting directory data sets and dynamically creates two new data sets to store the ACBs.

    The data set name must conform to the same naming convention as for a system-created directory data set.


    dataset_name (True, str, None)
      Describes the name of the data set.


    disposition (False, str, None)
      The status of the data set.


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


    volumes (False, list, None)
      A list of volume serials. When providing multiple volumes, processing will begin with the first volume in the provided list. Offline volumes are not considered.


    storage_class (False, str, None)
      The storage class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    management_class (False, str, None)
      The management class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    data_class (False, str, None)
      The data class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.



  temp_acb_dataset (False, dict, None)
    An optional control statement to define an empty work data set to be used as an IMS.ACBLIB data set for the IMS Catalog Populate utility.

    If IMS Management of ACBs is not enabled, this statement is ommitted.

    This data set does not need to conform to any IMS Catalog or system-defined naming convention.


    dataset_name (True, str, None)
      Describes the name of the data set.


    disposition (False, str, None)
      The status of the data set.


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


    volumes (False, list, None)
      A list of volume serials. When providing multiple volumes, processing will begin with the first volume in the provided list. Offline volumes are not considered.


    storage_class (False, str, None)
      The storage class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    management_class (False, str, None)
      The management class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    data_class (False, str, None)
      The data class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.



  directory_staging_dataset (False, dict, None)
    Optionally defines the size and placement IMS of the directory staging data set.

    The data set must follow the naming convention for the IMS Catalog Directory.


    dataset_name (True, str, None)
      Describes the name of the data set.


    disposition (False, str, None)
      The status of the data set.


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


    volumes (False, list, None)
      A list of volume serials. When providing multiple volumes, processing will begin with the first volume in the provided list. Offline volumes are not considered.


    storage_class (False, str, None)
      The storage class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    management_class (False, str, None)
      The management class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.


    data_class (False, str, None)
      The data class for an SMS-managed data set. Not valid for data sets that are not SMS-managed.



  proclib (True, list, None)
    Defines the IMS.PROCLIB data set that contains the DFSDFxxx member. The  DFSDFxxx member defines various attributes of the IMS catalog that are required by the utility.


  steplib (False, list, None)
    Points to IMS.SDFSRESL, which contains the IMS nucleus and required IMS modules.

    The steplib parameter can also be specified in the target inventory's environment\_vars.

    The steplib input parameter to the module will take precedence over the value specified in the environment\_vars.


  sysabend (False, str, None)
    Defines the dump data set. This defaults to = \\\*


  control_statements (False, dict, None)
    The control statement parameters.


    print_duplicate_resources (False, bool, False)
      Specifies that the DFS3PU00 utility lists each DBD or PSB resource in the input ACB library that is not added to the IMS catalog because it is a duplicate of an instance in the IMS catalog.

      Equivalent to the DUPLIST control statement.


    print_inserted_resources (False, bool, True)
      If the IMS management of ACBs is enabled, the utility also lists each DBD or PSB resources that is either added to the IMS directory or saved to the staging data set for importing into the IMS directory later.

      Equivalent to the ISRTLIST control statement.


    max_error_msgs (False, int, None)
      Terminate the IMS Catalog Populate utility when more than n messages indicate errors that prevent certain DBDs and PSBs from having their metadata that is written to the IMS catalog.

      Equivalent to the ERRORMAX=n control statement.


    resource_chkp_freq (False, int, None)
      Specifies the number of DBD and PSB resource instances to be inserted between checkpoints. n can be a 1 to 8 digit numeric value between 1 to 99999999.

      Equivalent to the RESOURCE\_CHKP\_FREQ=n control statement.


    segment_chkp_freq (False, int, None)
      Specifies the number of segments to be inserted between checkpoints. Can be a 1 to 8 digit numeric value between 1 to 99999999.

      Equivalent to the SEGMENT\_CHKP\_FREQ=n control statement.


    managed_acbs (False, dict, None)
      Use the managed\_acbs parameter to perform the following actions.

      Set up IMS to manage the runtime application control blocks for your databases and program views.

      Update an IMS system that manages ACBs with new or modified ACBs from an ACB library data set.

      Save ACBs from an ACB library to a staging data set for later importing into an IMS system that manages ACBs.


      setup (False, bool, None)
        Creates the IMS directory data sets that are required by IMS to manage application control blocks.


      stage (False, dict, None)
        Saves ACBs from the input ACB libraries to a staging data set.


        save_acb (False, str, None)
          If an ACB already exists in the IMS system, determines if it should be saved unconditionally or by the latest timestamp.


        clean_staging_dataset (False, bool, False)
          If the staging data set is not allocated to any online IMS system, scratch and recreate the staging data set before adding the resources to the staging data set.


        gsampcb (False, bool, False)
          GSAM resources are included for MANAGEDACBS= running in DLI mode using PSB DFSCP001.

          When GSAMPCB is specified, the IEFRDER batch log data set is not used by the catalog members information gather task.

          GSAMPCB and clean\_staging\_dataset are mutually exclusive.


        gsamdbd (False, str, None)
          The name of the changed GSAM database. You can use the gsamdbd variable with the STAGE or UPDATE parameter.

          LATEST, UNCOND, DELETE, SHARE, and GSAMPCB are not supported if you specify the gsamdbd variable.



      update (False, dict, None)
        Updates the existing IMS directory system data sets directly in exclusive mode. The ACBs are not placed in the staging data set.


        replace_acb (False, str, None)
          If an ACB already exists in the IMS system, determines if it should be overwritten unconditionally or by the latest timestamp.


        share_mode (False, bool, False)
          For dynamic option (DOPT) PSBs only, allocates the required IMS directory data sets in a shared mode so that the DOPT PSBs can be added to the IMS catalog without interrupting online processing.


        gsampcb (False, bool, False)
          GSAM resources are included for MANAGEDACBS= running in DLI mode using PSB DFSCP001. When GSAMPCB is specified, the IEFRDER batch log data set is not used by the catalog members information gather task.


        gsamdbd (False, str, None)
          The name of the changed GSAM database. You can use the gsamdbd variable with the STAGE or UPDATE parameter.

          LATEST, UNCOND, DELETE, SHARE, and GSAMPCB are not supported if you specify the gsamdbd variable.








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

    
    - name: Example of a loading the IMS Catalog running as a BMP
      ims_catalog_populate:
        online_batch: True
        ims_id: IMS1
        mode: LOAD
        acb_lib:
          - SOME.IMS.ACBLIB
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
        buffer_pool_param_dataset: "SOME.IMS.PROCLIB(DFSVSMHP)"
        dfsdf_member: "CAT"
        primary_log_dataset:
          dataset_name: SOME.IMS.LOG

    - name: Example of loading the IMS Catalog and the IMS Directory data sets with MANAGEDACBS enabled
      ims_catalog_populate:
        mode: LOAD
        acb_lib:
          - SOME.IMS.ACBLIB
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
        buffer_pool_param_dataset: "SOME.IMS.PROCLIB(DFSVSMHP)"
        dfsdf_member: "CAT"
        control_statements:
          managed_acbs:
            setup: true

    - name: Example of updating the IMS Catalog and staging libraries into the IMS directory staging data set
      ims_catalog_populate:
        mode: UPDATE
        acb_lib:
          - SOME.IMS.ACBLIB
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
        buffer_pool_param_dataset: "SOME.IMS.PROCLIB(DFSVSMHP)"
        dfsdf_member: "CAT"
        primary_log_dataset:
          dataset_name: SOME.IMS.LOG
        control_statements:
          managed_acbs:
            stage:
              save_acb: UNCOND
              clean_staging_dataset: true



Return Values
-------------

content (sometimes, str, DFS4434I INSTANCE 2020200562326 OF DBD AUTODB   WAS ADDED TO A NEWLY CREATED RECORD IN THE IMS CATALOG.)
  The standard output returned running the IMS Catalog Populate module.


rc (sometimes, str, 1)
  The return code from the IMS Catalog Populate utility.


stderr (sometimes, str, )
  The standard error output returned from running the IMS Catalog Populate utility.


msg (sometimes, str, You cannot define directory data sets, the bootstrap data set, or directory staging data sets with MANAGEDACBS=STAGE or MANAGEDACBS=UPDATE)
  Messages returned from the IMS Catalog Populate module.





Status
------





Authors
~~~~~~~

- Jerry Li (@th365thli)

