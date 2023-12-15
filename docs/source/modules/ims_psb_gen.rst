.. _ims_psb_gen_module:


ims_psb_gen -- Generate IMS PSB
===============================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The Program Specification Block (PSB) Generation utility places the created PSB in the PSB library so that it can be used by IMS application programs.






Parameters
----------

  src (False, str, None)
    The src field can reference a PDS, PDSE member, sequential data set, or UNIX System Services file path.

    If a PDS is specified, all members within the PDS will be treated as individual PSB source members to be processed.


  location (False, str, DATA_SET)
    The PSB source location, Supported options are DATA\_SET or USS. The default is DATA\_SET.

    The DATA\_SET option can be used for a PDS, PDSE, or sequential data set.


  replace (False, bool, True)
    When 'replace' is 'true', an existing PSB member matching the name in the input PSB source will be overwitten.


  member_list (False, raw, None)
    A list of member names if the source specified is a data set.

    Optionally, proceeding the source\_member, a colon with a target name for the generated PSB member can be specified. If no target name is specified, source\_name will be used as the target name.

    If 'member\_list' is empty and location is set to 'DATA\_SET' or not specified, then src is expected to be a sequential data set.

    Elements are of the list are str or dict with single key-value pair


  psb_name (False, str, None)
    Target name of the generated PSB member.

    This parameter is only required and applies if src is a sequential data set.


  batch (False, list, None)
    Batch can be used to perform multiple operations in a single module call.

    Expects a list of the location(s) of the IMS Program Specification Block (PSB) source to be compiled.

    The source can reference a PDS or PDSE member, sequential data set or UNIX System Services file path.


    src (False, str, None)
      The src field can reference a PDS, PDSE member, sequential data set, or UNIX System Services file path.

      If a PDS is specified, all members within the PDS will be treated as individual PSB source members to be processed.


    location (optional, str, DATA_SET)
      The PSB source location, Supported options are DATA\_SET or USS. The default is DATA\_SET.

      The DATA\_SET option can be used for a PDS, PDSE, or sequential data set.


    replace (False, bool, True)
      When 'replace' is 'true', an existing PSB member matching the name in the input PSB source will be overwitten.


    member_list (False, raw, None)
      A list of member names if the source specified is a data set.

      Optionally, proceeding the source\_member, a colon with a target name for the generated PSB member can be specified. If no target name is specified, source\_name will be used as the target name.

      If 'member\_list' is empty and location is set to 'DATA\_SET' or not specified, then src is expected to be a sequential data set.

      Elements are of the list are str or dict with single key-value


    psb_name (False, str, None)
      Target name of the generated PSB member.

      This parameter is only required and applies if src is a sequential data set.



  sys_lib (True, list, None)
    A list of required macro libraries that are needed to compile the PSB source. These libraries will be used as the sys\_lib at compile time.


  dest (True, str, None)
    The target output PSBLIB partitioned data set in which the PSB members will be generated.





Notes
-----

.. note::
   - Currently ims\_psb\_gen does not support copying symbolic links from both local to remote and remote to remote.




Examples
--------

.. code-block:: yaml+jinja

    
    ---
    - name: Basic example of IMS PSBGEN module with single data set
      ims_psb_gen:
        src: /tmp/src/somefile
        location: USS
        replace: true
        dest: SOME.DATA.SET.PSBLIB
        sys_lib:
        - SOME.DATA.SET.SDFSMAC
        - SYS1.MACLIB

    - name: Basic example of IMS PSBGEN module
      ims_psb_gen:
        batch:
        -
          src: /tmp/psbgen02
          location: USS
          replace: true
        -
          src: OMVSADM.IMSTESTU.ANSIBLE.PSB.SRC
          location: DATA_SET
          member_list: [PSBGENL : TARGET1, PSBGENL : TARGET2]
        -
          src: OMVSADM.IMSTESTU.ANSIBLE.PSB.SRC
          member_list: [PSBGENL, PSBGENL]
          replace: true
        -
          src: OMVSADM.IMSTESTU.ANSIBLE.PSB.SRC
          member_list:
          - 'COGPSBL': 'TARGET3'
          - 'COGPSBL2': 'TARGET4'
          replace: true
        -
          src: OMVSADM.IMSTESTU.ANSIBLE.PSB.SQ
          location: DATA_SET
          psb_name: SEQ
        dest: IMSBANK.IMS1.PSBLIB
        sys_lib:
        - IMSBLD.I15RTSMM.SDFSMAC
        - SYS1.MACLIB



Return Values
-------------

batch_result (on batch call, list, )
  List of output for each PSBGEN run on each element in the list of input source if input is batch.


  return_text (always, str, Invalid input source list being passed without content.)
    Status message.


  src (always, str, )
    input psb src name processed.



msg (always, str, PSBGEN execution was successful.)
  The message of the PSBGEN execution result.


rc (always, int, 0)
  Module return code (0 for success)


stderr (failure, str, Output data set for DDNAME has invalid record format.)
  Module standard error.


stdout (success, str, PSBGEN execution was successful.)
  Module standard output.





Status
------





Authors
~~~~~~~

- Ketan Kelkar (@ketan-kelkar) Omar Elbarmawi (@oelbarmawi)

