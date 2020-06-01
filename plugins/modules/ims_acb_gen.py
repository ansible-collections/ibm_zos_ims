#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}
DOCUMENTATION = r'''
---
module: ims_acb_gen
short_description: Generate IMS ACB
version_added: "2.9"
description:
  - The ims_acb_gen module generates an IMS application control block (ACB) necessary for an IMS application program to be scheduled and run. 
  - The ims_dbd_gen and ims_psb_gen modules can be used to generate the associated IMS database descriptors (DBDs) and program specification 
    block (PSBs) to be used with the ims_acb_gen module. 
  - The DBD and PSB control blocks will be merged and expanded into an IMS internal format called application control blocks (ACBs).

author:
  - Dipti Gandhi (@ddgandhi)
  - Jerry Li (@th365thli)
options:
  command_input:
    description:
      - This field specifies two command options(BUILD/DELETE).
      - BUILD - Specifies that blocks are built for the named PSBs, which refer to the named DBDs.
      - DELETE - Specifies that blocks are deleted from the ACBLIB data set. The named PSBs and all PSBs that refer to the named DBDs are deleted.
    required: true
    type: str
    choices:
      - BUILD
      - DELETE
  compression:
    description:
      - PRECOMP,POSTCOMP, in any combination, cause the required in-place compression.
      - The default is none.
    type: str
    required: false
    default: none
  psb_name:
    description:
      - The name of the PSB(s). Specifies that blocks are built or deleted for all PSBs that are named on this control statement.
      - This field requires "ALL" or a list of psb names to be specified.
    required: false
    type: list
  dbd_name:
    description:
      - The name of the DBD(s). Specifies that blocks are built or deleted for this DBD, and for all PSBs that reference this DBD either directly or indirectly through logical relationships.
    required: false
    type: list
  acb_lib:
    description:
      - The ACB Maintenance utility maintains the prebuilt blocks (ACB) library (IMS.ACBLIB). The ACB library is a consolidated library of program (PSB) and database (DBD) descriptions.
      - The IMS acb_lib must be used exclusively. The module can only be executed using an ACB library which is not concurrently allocated to an active IMS system.
    required: true
    type: str
  psb_lib:
    description:
      - The ACB Maintenance utility receives input from the IMS PSBLIB data set.
      - The ACB Maintenance utility does not change the PSB(s) in PSBLIB. If changes are made in PSBs or DBDs that require changes in the associated PSB,
        make these changes before running the module.
      - Changes in PSBs might also require modifications to the affected application programs. For example, if a DBD has a segment name changed,
        all PSBs which are sensitive to that segment must have their SENSEG statements changed.
    required: true
    type: list
  dbd_lib:
    description:
      - The ACB Maintenance utility receives input from the IMS DBDLIB data set.
      - The ACB Maintenance utility does not change the DBD(s) in DBDLIB. If changes are made in PSBs or DBDs that require changes in the associated DBD,
        make these changes before running the module.
    required: true
    type: list
  steplib:
    description:
      - Points to the IMS SDFSRESL data set, which contains the IMS nucleus and required IMS modules. If STEPLIB is unauthorized by having unauthorized libraries 
        that are concatenated to SDFSRESL, you must specify the I(reslib) parameter. 
      - The steplib parameter can also be specified in the target inventory's environment_vars. 
      - The steplib input parameter to the module will take precedence over the value specified in the environment_vars.  
    required: false
    type: list
  reslib:
    description:
      - Points to an authorized library that contains the IMS SVC modules. For IMS batch, SDFSRESL and any data set that is concatenated to it in the 
        reslib field must be authorized through the Authorized Program Facility (APF).
    required: false 
    type: list
  build_psb:
    description:
      - Specifies whether ims_acb_gen rebuilds all PSBs that reference a changed DBD in the I(dbdname) parameter.
      - TRUE indicates that ims_acb_gen rebuilds all PSBs that reference the changed DBD on the I(dbdname) parameter.
      - FALSE indicates that ims_acb_gen does not rebuild PSBs that reference the changed DBD if the changed DBD does not change the physical structure of the database.
    required: false
    type: bool
    default: true
notes:
  - The I(steplib) parameter can also be specified in the target inventory's environment_vars. 
  - The I(steplib) input parameter to the module will take precedence over the value specified in the environment_vars.
  - If only the I(steplib) parameter is specified, then only the I(steplib) concatination will be used to resolve the IMS RESLIB dataset. 
  - If both I(steplib) and I(reslib) are specified, then both parameters will be used by the ACB Maintenenace Utility and I(reslib) will be used to resolve the IMS RESLIB dataset. 
  - Specifying only I(reslib) without I(steplib) is not supported. 
  - The ACB Maintenenace utility SYSUT3/SYSUT4 DD options are not supported by this module.
  - The current implementation of the ims_acb_gen module requires a jobcard to be specified using the JOB_CARD variable in the target inventory's group variables. 
    See the sample L(group_vars,https://github.com/ansible-collections/ibm_zos_ims/blob/master/playbooks/group_vars/all.yml) provided with our sample playbook for an example of 
    the JOB_CARD variable. 
'''

EXAMPLES = r'''
- name: Example of creating ACBs for specific PSBs.
  ims_acb_gen:
    command_input: BUILD
    COMPRESSION: PRECOMP,POSTCOMP
    psb_name:
      - PSB1
      - PSB2
      - PSB3
    dbd_name:
      - DBD1
      - DBD2
    psb_lib:
      - SOME.IMS.PSBLIB1
      - SOME.IMS.PSBLIB2
    dbd_lib:
      - SOME.IMS.DBDLIB1
      - SOME.IMS.DBDLIB2
      - SOME.IMS.DBDLIB3
    acb_lib: SOME.IMS.ACBLIB
    reslib:
      - SOME.IMS.SDFSRESL1
      - SOME.IMS.SDFSRESL2
    steplib:
      - SOME.IMS.SDFSRESL1
      - SOME.IMS.SDFSRESL2
    build_psb: false  

- name: Example of creating blocks for all PSBs in the psb_lib data set.
  ims_acb_gen:
    command_input: BUILD
    psb_name: ALL
    psb_lib:
      - SOME.IMS.PSBLIB1
    dbd_lib:
      - SOME.IMS.DBDLIB1
    acb_lib: SOME.IMS.ACBLIB
    
- name: Example of deleting PSBs and DBDs
  ims_acb_gen:
    command_input: DELETE
    psb_name:
      - PSB1
    dbd_name:
      - DBD1
      - DBD2
      - DBD3
      - DBD4
      - DBD5
      - DBD6
    acb_lib: SOME.IMS.ACBLIB
    reslib:
      - SOME.IMS.SDFSRESL1
'''

RETURN = r'''
msg:
  description: Execution result message from the ims_acb_gen module.
  returned: always
  type: str
  sample: ACBGEN execution is successful.
content:
  description: The response from the execution of the ACB Maintenance Utility.
  returned: always
  type: list
rc:
  description: The resulting return code from the ACB Maintenance Utility.
  returned: always
  type: str
  sample: '0'
changed:
  description:
    - Indicates if any changes were made during module execution.
    - True is always returned unless a module or failure has occurred.
  returned: always
  type: bool
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_ims.plugins.module_utils.ims_gen_utils import (
    submit_uss_jcl,
)


def run_module():
    module_args = dict(
        command_input=dict(type="str", required=True),
        compression=dict(type="str", required=False, default=""),
        psb_name=dict(type="list", elements="str", required=False),
        dbd_name=dict(type="list", elements="str", required=False),
        acb_lib=dict(type="str", required=True),
        psb_lib=dict(type="list", required=True),
        dbd_lib=dict(type="list", required=True),
        reslib=dict(type="list", required=False),
        steplib=dict(type="list", required=False),
        build_psb=dict(type="bool", required=False, default=True),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    result = dict(rc="0", jobId="")
    jobId = submit_uss_jcl(module)
    result["jobId"] = jobId
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
