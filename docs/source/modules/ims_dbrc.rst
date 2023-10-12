.. _ims_dbrc_module:


ims_dbrc -- Submit IMS DBRC Commands
====================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Use Database Recovery Control (DBRC) to record and manage information that is stored in a set of VSAM data sets that are collectively called the Recovery Control (RECON) data set.

Based on this information, you can use DBRC to advise IMS about how to proceed with certain IMS actions.






Parameters
----------

  command (True, list, None)
    This is the well-formatted DBRC command to submit.


  dbd_lib (False, str, None)
    The data set that contains the descriptions for the databases that are under the control of DBRC.


  dynamic_allocation_dataset (False, str, None)
    The dynamic allocation data set that will be used to complete the DBRC execution.

    Required if \`recon1\`, \`recon2\`, and \`recon3\` are not specified.


  genjcl_input_dataset (False, str, None)
    The PDS, which contains the skeletal JCL members used by the DBRC utility to generate JCL.

    Equivalent to the JCLPDS control statement.


  genjcl_output_dataset (False, str, None)
    The data set which is to receive the generated JCL. It is required only for the GENJCL commands.

    Equivalent to the JCLOUT control statement.


  max_rc (False, int, None)
    The maximum acceptable return code allowed for the module to complete succesfully.


  recon1 (False, str, None)
    The RECON1 data set that will be used to complete the DBRC execution.

    Required if \`dynamic\_allocation\_dataset\` is not specified.


  recon2 (False, str, None)
    The RECON2 data set that will be used to complete the DBRC execution.

    Required if \`dynamic\_allocation\_dataset\` is not specified.


  recon3 (False, str, None)
    The RECON3 data set that will be used to complete the DBRC execution.

    Required if \`dynamic\_allocation\_dataset\` is not specified.


  steplib (True, list, None)
    List of STEPLIB datasets that contain the IMS nucleus and the required action modules.





Notes
-----

.. note::
   - The \ :emphasis:`steplib`\  parameter can also be specified in the target inventory's environment\_vars.
   - The \ :emphasis:`steplib`\  input parameter to the module will take precedence over the value specified in the environment\_vars.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Sample DBRC Single Command
      ims_dbrc:
        command: LIST.RECON STATUS
        steplib:
          - IMSTESTU.IMS1501.MARKER
          - IMSTESTL.IMS1.EXITLIB
          - IMSTESTG.IMS15R.TSTRES
          - IMSBLD.IMS15R.USERLIB
          - IMSBLD.I15RTSMM.CRESLIB
        dbd_lib: IMSTESTL.IMS1.DBDLIB
        genjcl_input_dataset: IMSTESTL.IMS1.GENJCL
        genjcl_output_dataset: IMSTESTL.IMS1.JCLOUT
        dynamic_allocation_dataset: IMSTESTL.IMS1.DYNALLOC

    - name: Sample DBRC Multiple Commands with dynamic_allocation_dataset Specified
      ims_dbrc:
        command:
          - LIST.RECON STATUS
          - LIST.DB ALL
          - LIST.DBDS DBD(CUSTOMER)
        steplib:
          - IMSTESTU.IMS1501.MARKER
          - IMSTESTL.IMS1.EXITLIB
          - IMSTESTG.IMS15R.TSTRES
          - IMSBLD.IMS15R.USERLIB
          - IMSBLD.I15RTSMM.CRESLIB
        dbd_lib: IMSTESTL.IMS1.DBDLIB
        genjcl_input_dataset: IMSTESTL.IMS1.GENJCL
        genjcl_output_dataset: IMSTESTL.IMS1.JCLOUT
        dynamic_allocation_dataset: IMSTESTL.IMS1.SDFSRESL

    - name: Sample DBRC Multiple Commands with RECON specified
      ims_dbrc:
        command:
          - LIST.RECON STATUS
          - INIT.DB DBD(TESTDB)
          - DELETE.DB DBD(TESTDB)
        steplib:
          - IMSTESTU.IMS1501.MARKER
          - IMSTESTL.IMS1.EXITLIB
          - IMSTESTG.IMS15R.TSTRES
          - IMSBLD.IMS15R.USERLIB
          - IMSBLD.I15RTSMM.CRESLIB
        dbd_lib: IMSTESTL.IMS1.DBDLIB
        genjcl_input_dataset: IMSTESTL.IMS1.GENJCL
        genjcl_output_dataset: IMSTESTL.IMS1.JCLOUT
        recon1: IMSTESTL.IMS1.RECON1
        recon2: IMSTESTL.IMS1.RECON2
        recon3: IMSTESTL.IMS1.RECON3



Return Values
-------------

dbrc_output (sometimes, list, )
  The output provided by the specified DBRC Command(s).


  command (always, str, )
    The original submitted command that corresponds to the output.


  messages (always, list, )
    Compiled list of messages returned from the DBRC output.


  output (always, dict, )
    Parsed DBRC output that maps each field to its corresponding value.



msg (always, str, )
  The output message that the \`ims\_dbrc\` module generates.


rc (always, int, )
  The return code returned by the DBRC module.


unformatted_output (always, list, )
  Unformatted output response from the all of the submitted DBRC commands.





Status
------





Authors
~~~~~~~

- Omar Elbarmawi (@oelbarmawi)

