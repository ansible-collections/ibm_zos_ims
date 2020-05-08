# -*- coding: utf-8 -*-

from pprint import pprint
import pytest

__metaclass__ = type

def test_ims_command_sample(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_command(command='QUERY PGM', plex="PLEX1", route="IMS1")
    for result in results.contacted.values():
        pprint(result)