=============================
ibm.ibm_zos_ims Release Notes
=============================

.. contents:: Topics


v1.2.0
======

Release Summary
---------------

Release Date: '2023-03-31'
This changelog describes all changes made to the modules and plugins included
in this collection.
For additional details such as required dependencies and availability review
the collections `release notes <https://github.com/ansible-collections/ibm_zos_ims/blob/dev/docs/source/release_notes.rst>`__ 


Major Changes
-------------

- Adds support for Ansible 4 (ansible-core 2.11)
- DBDGEN sample2 testcase file was deleted since it was a duplicate and contained an invalid testcase
- Fixed bug in ims_catalog_populate module where check_timestamp was false would cause module calls to return an IMS error
- Fixed sanity test error for ims_dbdgen and ims_psbgen modules after the member_list argument type was updated to 'raw' from 'list' since the element type can either be str or key:value pair
- Improved JSON keys for ims_command_utils to replace whitespaces with underscores to help make the output more parsable

v1.1.0
======

Major Changes
-------------

- Improved test and security coverage
- Removed dependency on Requests library for Python on the control node.
- ims_catalog_populate - improved pep8 and Ansible Sanity compliance
- ims_catalog_purge - improved pep8 and Ansible Sanity compliance
- ims_dbd_gen - added usage of Python tempdir libraries instead of fixed string
- ims_dbrc - improved pep8 and Ansible Sanity compliance
- ims_psb_gen - added usage of Python tempdir libraries instead of fixed string

New Modules
-----------

- ibm.ibm_zos_ims.ims_catalog_populate - Add records to the  IMS Catalog
- ibm.ibm_zos_ims.ims_catalog_purge - Purge records from the IMS Catalog
- ibm.ibm_zos_ims.ims_dbrc - Submit IMS DBRC Commands

v1.0.1
======

Major Changes
-------------

- Enhancement for ims_acb_gen, ims_dbd_gen and ims_psb_gen modules
- Improved test and security coverage
- Updated sample playbook

New Modules
-----------

- ibm.ibm_zos_ims.ims_acb_gen - Generate IMS ACB
- ibm.ibm_zos_ims.ims_command - Submit IMS Commands
- ibm.ibm_zos_ims.ims_dbd_gen - Generate IMS DBD
- ibm.ibm_zos_ims.ims_psb_gen - Generate IMS PSB
