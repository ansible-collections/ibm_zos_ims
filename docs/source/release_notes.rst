.. ...........................................................................
.. © Copyright IBM Corporation 2025                                          .
.. ...........................................................................

========
Releases
========

Version 1.3.1
=============

Notes
-----

 * Compatibility to the latest dependencies versions

   * Support for z/OS core v1.10 or later.
   * Support for Python v3.11 or later.
   * Support for ZOAU v1.3.0 or later.
   * Support for Ansible 2.15 or later.


Availability
------------

* `Automation Hub`_
* `Galaxy`_
* `GitHub`_

Reference
---------

* Supported by IBM IMS through v15.5.
* Supported by IBM z/OS core collection v1.10.0 or later.
* Supported by IBM Z Open Enterprise Python for z/OS v3.11 - v3.13.
* Supported by IBM Z Open Automation Utilities (ZOAU) v1.3.0 or later.

  *  ZOAU minimum supported version may vary depending on the z/OS core collection version that is chosen. For details on z/OS core collection requirements, see `z/OS Core Releases`_.
* Supported by z/OS V2R5 (or later)
* The z/OS® shell

Version 1.3.0
=============

Notes
-----

* New module

  * ``ims_ddl``

    * The IMS Data Definition utility (DFS3ID00) utility writes the metadata for your application programs (PSBs) and databases definitions to the IMS Catalog records and the runtime blocks to the staging directory dataset.

* Bug fixes and enhancements

  * Added new member ``dfsdf_member`` in the ``ims_catalog_populate`` and ``ims_catalog_purge`` modules.
    The DFSDFxxx member is in the IMS.PROCLIB data set where the CATALOG section is defined.

* Documentation updates

  * Minor updates to ``compression`` parameter in the ``ims_acbgen`` module where PRECOMP,POSTCOMP, in any combination, cause the required in-place compression.
    The choices are not mutually exclusive -- PRECOMP or POSTCOMP or PRECOMP,POSTCOMP can be used.

* Improved test and ansible-sanity coverage.
* Subset of the test cases were updated to support for Ansible 2.15.
* Additional support for test cases in ``ims_catalog_populate`` and ``ims_catalog_purge`` modules to support ``dfsdf_member`` parameter.
* Source ``type()`` was replaced by ``isinstance()`` in the code for gen utilities since ansible-core 2.16 supports Python 3.12 and that version deprecated ``type()`` function.
* This update also has updated prerequisites for Ansible 2.14 or later and ZOAU 1.2.2 or later but prior to version 1.3.

Availability
------------

* `Automation Hub`_
* `Galaxy`_
* `GitHub`_

Reference
---------

* Supported by IBM z/OS core collection v1.5.0 or later.
* Supported by IBM Z Open Enterprise Python for z/OS v3.9 - v3.12.
* Supported by IBM Z Open Automation Utilities 1.2.2 or later (but prior to 1.3).

  * ZOAU minimum supported version may vary depending on the z/OS core collection version that is chosen. For details on z/OS core collection requirements, see `z/OS Core Releases`_.
* Supported by z/OS V2R4 (or later) but prior to version V3R1.
* The z/OS® shell.

.. .............................................................................
.. Global Links
.. .............................................................................

.. _Automation Hub:
   https://www.redhat.com/en/technologies/management/ansible/automation-hub?sc_cid=7015Y000003t7aWQAQ

.. _GitHub:
   https://github.com/ansible-collections/ibm_zos_ims

.. _Galaxy:
   https://galaxy.ansible.com/ibm/ibm_zos_ims

.. _z/OS Core Releases:
   https://github.com/ansible-collections/ibm_zos_core/releases

