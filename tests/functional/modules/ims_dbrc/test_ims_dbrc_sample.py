# -*- coding: utf-8 -*-

from pprint import pprint
import pytest

__metaclass__ = type

def test_ims_dbrc_sample(ansible_zos_module):
    hosts = ansible_zos_module
    results = hosts.all.ims_dbrc(
        command=[
            "LIST.RECON STATUS", 
            "LIST.DB ALL",
            "LIST.BKOUT ALL",
            "LIST.LOG",
            "LIST.CAGRP"],
        steplib=[
            "IMSTESTU.IMS1501.MARKER",
            "IMSBANK2.IMS1.EXITLIB",
            "IMSTESTG.IMS15R.TSTRES",
            "IMSBLD.IMS15R.USERLIB",
            "IMSBLD.I15RTSMM.CRESLIB"],
        dbdlib="IMSBANK2.IMS1.DBDLIB",
        genjcl="IMSTESTL.IMS1.GENJCL",
        recon1="IMSBANK2.IMS1.RECON1",
        recon2="IMSBANK2.IMS1.RECON2",
        recon3="IMSBANK2.IMS1.RECON3"
    )
    for result in results.contacted.values():
        pprint(result)
        assert False