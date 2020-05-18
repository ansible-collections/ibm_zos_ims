#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r'''
---

module: ims_dbrc

short_description: Submit IMS Database Recovery Control (DBRC) Commands
version_added: "2.9"

description:
  - Use DBRC to record and manage information that is stored in a set of VSAM
    data sets that are collectively called the Recovery Control (RECON) data set.
  - Based on this information, you can use DBRC to advise IMS about how to proceed
    for certain IMS actions.
author:
  - Omar Elbarmawi (@oelbarmawi)
options:
  batch:
    description:
      - submit multiple IMS commands with a single invocation of the module.
    required: false
    type: list
    elements: dict
    suboptions:
      command:
        description:
          - This is the (well-formatted) DBRC API command to submit.
        type: str
        required: true
      plex:
        description:
          - Specify the IMSPLEX in which the IMS Command will be submitted.
        type: str
        required: true
      route:
        description:
          - Specify the IMS System in which the IMS Command will be submitted.
          - Leaving this field empty will result in invoking all available routes within the specified PLEX.
        type: list
        required: false
  command:
    description:
      - This is the (well-formatted) DBRC API command to submit.
    type: str
    required: true
  plex:
    description:
      - Specify the IMSPLEX in which the IMS Command will be submitted.
    type: str
    required: true
  route:
    description:
      - Specify the IMS System in which the IMS Command will be submitted.
      - Leaving this field empty will result in invoking all available routes within the specified PLEX.
    type: list
    required: false
'''

EXAMPLES = '''
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
'''