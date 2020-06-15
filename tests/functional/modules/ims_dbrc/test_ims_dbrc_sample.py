# -*- coding: utf-8 -*-

from pprint import pprint
import pytest

__metaclass__ = type

def test_ims_dbrc_sample(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(command='LIST.RECON STATUS', steplib="whatever")
    for result in results.contacted.values():
        pprint(result)
        assert False