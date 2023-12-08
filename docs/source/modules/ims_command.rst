.. _ims_command_module:


ims_command -- Submit IMS Commands
==================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Submit Type 1 and Type 2 IMS Commands. User specifies a well formatted IMS Command string along with PLEX and (optional) ROUTE information.

IMS will return a completion code, return code, and reason code along with any relevant text indicating the status of the command that was run.






Parameters
----------

  batch (False, list, None)
    submit multiple IMS commands with a single invocation of the module.


    command (True, str, None)
      This is the (well-formatted) command to submit to IMS Batch.


    plex (True, str, None)
      Specify the IMSPLEX in which the IMS Command will be submitted.


    route (False, list, None)
      Specify the IMS System in which the IMS Command will be submitted.

      Leaving this field empty will result in invoking all available routes within the specified PLEX.



  command (False, str, None)
    This is the (well-formatted) command to submit to IMS Batch.


  plex (False, str, None)
    Specify the IMSPLEX in which the IMS Command will be submitted.


  route (False, list, None)
    Specify the IMS System in which the IMS Command will be submitted.

    Leaving this field empty will result in invoking all available routes within the specified PLEX.





Notes
-----

.. note::
   - This module requires Structured Call Interface (SCI) and Operations Manager (OM) to be active in the target IMSplex.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Query all programs for IMS1 in PLEX1
      ims_command:
        command: QUERY PGM SHOW(ALL)
        plex: PLEX1
        route: IMS1

    - name: Query all programs for IMS1 and IMS2 in PLEX1
      ims_command:
        command: QUERY PGM SHOW(ALL)
        plex: PLEX1
        route: ['IMS1', 'IMS2']

    - name: Query all transactions for all routes in PLEX1
      ims_command:
        command: QUERY TRAN SHOW(ALL)
        plex: PLEX1

    - name: Stop all transactions for IMS2 in PLEX1
      ims_command:
        command: UPDATE TRAN STOP(Q)
        plex: PLEX1
        route: IMS2

    - name: Create a DB called IMSDB1 for IMS3 in PLEX2
      ims_command:
        command: CREATE DB NAME(IMSDB1)
        plex: PLEX2
        route: IMS3

    - name: Batch call - query all pgms, create pgm, and query for new
      ims_command:
        batch:
          -
            command: QUERY PGM SHOW(ALL)
            plex: PLEX1
            route: IMS1
          -
            command: CREATE PGM NAME(EXAMPLE1)
            plex: PLEX1
            route: IMS1
          -
            command: QUERY PGM SHOW(ALL)
            plex: PLEX1
            route: IMS1



Return Values
-------------

failed (always, bool, )
  Indicates the outcome of the module.


ims_output (sometimes, list, )
  The output provided by the specified IMS Command. All the IMS return, reason, and completion codes from running the commands along with associated text.


  ims_member_data (sometimes, dict, )
    Output from Type 1 commands.


  ims_member_messages (sometimes, dict, )
    Messages from the IMS instance in which the command was routed.


  return_codes (always, dict, )
    Return codes indicating the general result of running the IMS command.


    imsrc (, str, )
      General IMS return code.


    reason (, str, )
      Return code indicating specific status of the command.


    results (, str, )
      Return code indicating the results of the command.



  subgroup_info (always, dict, )
    Returns output from the OM instance in which the command was routed.


    ctl.rc (, str, )
      Return code (i.e. 0000000).


    ctl.rsn (, str, )
      CTL reason code.



  type_2_data (sometimes, dict, )
    Data resulting from the output of the IMS command submitted.


    CC (, str, )
      Completion code for the line of output. Completion code is always returned.


    CCText (, str, )
      Completion code text that describes the meaning of the nonzero completion code.







Status
------





Authors
~~~~~~~

- Ketan Kelkar (@ketankelkar)
- Jerry Li (@th365thli)
- Omar Elbarmawi (@oelbarmawi)

