.. _ims_dbd_gen_module:


ims_dbd_gen -- Generate IMS DBD
===============================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This ims\_dbd\_gen module generates IMS database descriptor (DBD) resource(s) to define a database so that it can be used by IMS application programs.

A database descriptor (DBD) is a DL/I control block describing the database, segments, fields, indexes and relationships.

Generating a DBD is a two step process that assembles the DBD source and binds it into a database definition.






Parameters
----------

  src (False, str, None)
    The src field can reference a PDS, PDSE member, sequential data set, or UNIX System Services file path.

    If a PDS is specified, all members within the PDS will be treated as individual DBD source members to be processed.


  location (False, str, DATA_SET)
    The DBD source location. Supported options are DATA\_SET or USS. The default is DATA\_SET.

    The DATA\_SET option can be used for a PDS, PDSE, or sequential data set.


  replace (False, bool, True)
    When 'replace' is 'true', an existing DBD member matching the name in the

    input DBD source will be overwitten.


  member_list (False, raw, None)
    A list of member names if the source specified is a data set.

    Optionally, proceeding the source\_member, a colon with a target name for the generated DBD member can be specified. If no target name is specified, source\_name will be used as the target name.

    If 'member\_list' is empty and location is set to 'DATA\_SET' or not specified, then src is expected to be a sequential data set.

    Elements are of the list are str or dict with single key-value pair


  dbd_name (False, str, None)
    Target name of the generated DBD member.

    This parameter is only required and applies if src is a sequential data set.


  batch (False, list, None)
    Batch can be used to perform multiple operations in a single module call.

    Expects a list of the location(s) of the IMS Database Descriptor (DBD) source to be compiled.

    The source can reference a PDS or PDSE member, sequential data set or UNIX System Services file path.


    src (False, str, None)
      The src field can reference a PDS, PDSE member, sequential data set, or UNIX System Services file path.

      If a PDS is specified, all members within the PDS will be treated as individual DBD source members to be processed.


    location (False, str, DATA_SET)
      The DBD source location. Supported options are DATA\_SET or USS. The default is DATA\_SET.

      The DATA\_SET option can be used for a PDS, PDSE, or sequential data set.


    replace (False, bool, True)
      When 'replace' is 'true', an existing DBD member matching the name in the input DBD source will be overwitten.


    member_list (False, raw, None)
      A list of member names if the source specified is a data set.

      Optionally, proceeding the source\_member, a colon with a target name for the generated DBD member can be specified. If no target name is specified, source\_name will be used as the target name.

      If 'member\_list' is empty and location is set to 'DATA\_SET' or not specified, then src is expected to be a sequential data set.

      Elements are of the list are str or dict with single key-value pair


    dbd_name (False, str, None)
      Target name of the generated DBD member.

      This parameter is only required and applies if src is a sequential data set.



  sys_lib (True, list, None)
    A list of required macro libraries that are needed to compile the DBD source. These libraries will be used as the sys\_lib at compile time.


  dest (True, str, None)
    The target output DBDLIB partitioned data set where the DBD members will be generated to.





Notes
-----

.. note::
   - Currently ims\_dbd\_gen does not support copying symbolic links from both local to remote and remote to remote.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Basic example of IMS DBDGEN module with a single USS source.
      ims_dbd_gen:
        src: /tmp/src/somefile
        location: USS
        'replace': true
        dest: SOME.PARTITIONED.DATA.SET.DBDLIB
        sys_lib:
          - SOME.DATA.SET.SDFSMAC
          - SYS1.MACLIB
    - name: Basic example of IMS DBDGEN module with a single sequential data set.source.
      ims_dbd_gen:
        src: SOME.DATA.SET.DBD
        'replace': true
        dest: SOME.PARTITIONED.DATA.SET.DBDLIB
        dbd_name: exampleDBD
        sys_lib:
          - SOME.DATA.SET.SDFSMAC
          - SYS1.MACLIB
    - name: Basic example of IMS DBDGEN module with a single PDS source.
      ims_dbd_gen:
        src: SOME.DATA.SET.DBD.SRC
        'replace': true
        member_list:
          - 'DEDBJN21': 'DBD1'
          - 'DEDBJN21': 'DBD2'
          - 'DEDBJNV1': 'DBD3'
        dest: SOME.PARTITIONED.DATA.SET.DBDLIB
        sys_lib:
          - SOME.DATA.SET.SDFSMAC
          - SYS1.MACLIB
    - name: Basic example of IMS DBDGEN module with a batch input uniform source type.
      ims_dbd_gen:
        batch:
          -
            src: /tmp/src/somefile1
            location: USS
            'replace': true
          -
            src: /tmp/src/somefile2
            location: USS
            'replace': true
        dest: SOME.PARTITIONED.DATA.SET.DBDLIB
        sys_lib:
          - SOME.DATA.SET.SDFSMAC
          - SYS1.MACLIB
    - name: Basic example of IMS DBDGEN module with a batch input varied source type.
      ims_dbd_gen:
        batch:
          -
            src: /tmp/src/somefile
            location: USS
            'replace': true
          -
            src: SOME.DATA.SET.DBD.SRC
            location: DATA_SET
            member_list: [DSMEMBR1, DSMEMBR2 : target2, DSMEMBR3]
          -
            src: SOME.DATA.SET.DBD.SRC
            member_list: [DSMEMBR4 : target4]
            'replace': true
          -
            src: SOME.DATA.SET.DBD.SEQ
            location: DATA_SET
            dbd_name: SEQ
        dest: SOME.PARTITIONED.DATA.SET.DBDLIB
        sys_lib:
          - SOME.DATA.SET.SDFSMAC
          - SYS1.MACLIB



Return Values
-------------

batch_result (on batch call, list, )
  List of output for each DBDGEN run on each element in the list of input source if input is batch.


  return_text (always, str, Invalid input source list being passed without content.)
    Status message.


  src (always, str, )
    input dbd src name processed.



msg (always, str, DBDGEN execution was successful.)
  The message of the DBDGEN execution result.


rc (always, int, 0)
  Module return code (0 for success)


stderr (failure, str, Output data set for DDNAME has invalid record format.)
  Module standard error


stdout (success, str, DBDGEN execution was successful)
  Module standard output





Status
------





Authors
~~~~~~~

- Seema Phalke (@sphalke) Dipti Gandhi (@ddgandhi)

