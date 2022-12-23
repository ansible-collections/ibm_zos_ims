.. ...........................................................................
.. © Copyright IBM Corporation 2020                                          .
.. ...........................................................................

========
Releases
========


Version 1.2.0-beta.2
====================

Notes
-----

* Update recommended
* Bug fixes and enhancements

  * Fixed sanity test error for ``dbdgen`` and ``psbgen`` modules after the member_list argument type was updated to ``raw`` from ``list`` since the element type can either be str or key:value pair.
  * DBDGEN sample2 testcase file was deleted since it was a duplicate and contained an invalid testcase.
  * This update also has updated prerequisites for Ansible 2.11 and ZOAU 1.1.1.

Availability
------------

* `Galaxy`_
* `GitHub`_

Reference
---------

* Supported by IBM z/OS core collection v1.4.0 or later
* Supported by IBM Z Open Enterprise Python for z/OS: v3.8, v3.9 
* Supported by IBM Z Open Automation Utilities 1.1.1 PTF
* Supported by z/OS V2R3
* The z/OS® shell

.. _centralized content:
   https://ibm.github.io/z_ansible_collections_doc/index.html

.. _GitHub:
   https://github.com/ansible-collections/ibm_zos_ims

.. _Galaxy:
   https://galaxy.ansible.com/ibm/ibm_zos_ims

Version 1.2.0-beta.1
====================

Notes
-----

* Update recommended
* Bug fixes and enhancements

  * Adds support for Ansible 4 (ansible-core 2.11)
  * Fixed bug in ``ims_catalog_populate`` where ``check_timestamp: false`` would cause module calls to return an IMS error.
  * Improved JSON keys for ``ims_command_utils`` to replace whitespaces with underscores to help make the output more parsable.
  * This update also has updated prerequisites for Ansible 2.11 and ZOAU 1.1.0 or later.

Availability
------------

* `Galaxy`_
* `GitHub`_

Reference
---------

* Supported by IBM z/OS core collection v1.3.0 or later
* Supported by IBM Z Open Enterprise Python for z/OS: 3.8.2 or later
* Supported by IBM Z Open Automation Utilities 1.1.0 PTF or later
* Supported by z/OS V2R3
* The z/OS® shell

.. _centralized content:
   https://ibm.github.io/z_ansible_collections_doc/index.html

.. _GitHub:
   https://github.com/ansible-collections/ibm_zos_ims

.. _Galaxy:
   https://galaxy.ansible.com/ibm/ibm_zos_ims

Version 1.1.0
====================

Notes
-----

  * Update recommended
  * Module changes

    * ``ims_catalog_populate`` - improved pep8 and Ansible Sanity compliance
    * ``ims_catalog_purge`` - improved pep8 and Ansible Sanity compliance
    * ``ims_dbrc`` - improved pep8 and Ansible Sanity compliance
    * ``ims_dbd_gen`` - added usage of Python tempdir libraries instead of fixed string
    * ``ims_psb_gen`` - added usage of Python tempdir libraries instead of fixed string
  * Documentation updates
  * Improved test and security coverage

Availability
------------

  * `Automation Hub`_
  * `Galaxy`_
  * `GitHub`_

Reference
---------

  * Supported by IBM z/OS core collection v1.2.1
  * Supported by IBM Z Open Enterprise SDK for Python for z/OS: 3.8.2 or later
  * Supported by IBM Z Open Automation Utilities 1.0.3 PTF UI70435
  * Supported by z/OS V2R3
  * The z/OS® shell

.. _Automation Hub:
   https://www.ansible.com/products/automation-hub

.. _Galaxy:
   https://galaxy.ansible.com/ibm/ibm_zos_ims

.. _GitHub:
   https://github.com/ansible-collections/ibm_zos_ims

Version 1.0.1
====================

Notes
-----

  * Update recommended

    * ``ims_acb_gen``
    * ``ims_dbd_gen``
    * ``ims_psb_gen``
    * ``ims_command``
  * Documentation updates
  * Improved test and security coverage

Availability
------------

  * `Automation Hub`_
  * `Galaxy`_
  * `GitHub`_

Reference
---------

  * Supported by IBM z/OS core collection v1.2.1 or later
  * Supported by IBM Z Open Enterprise Python for z/OS: 3.8.2 or later
  * Supported by IBM Z Open Automation Utilities 1.0.3 PTF UI70435 or later
  * Supported by z/OS V2R3
  * The z/OS® shell

.. _Automation Hub:
   https://www.ansible.com/products/automation-hub

.. _Galaxy:
   https://galaxy.ansible.com/ibm/ibm_zos_ims

.. _GitHub:
   https://github.com/ansible-collections/ibm_zos_ims

Version 1.1.0-beta.1
====================

Notes
-----

* Update recommended
* New modules

  * ``ims_catalog_populate``
  * ``ims_catalog_purge``
  * ``ims_dbrc``
* Documentation

  * Update documentation in support of `centralized content`_.
* Updated sample playbook

Availability
------------

* `Galaxy`_
* `GitHub`_

Reference
---------

* Supported by IBM z/OS core collection v1.2.0-beta.1 or later
* Supported by IBM Z Open Enterprise Python for z/OS: 3.8.2 or later
* Supported by IBM Z Open Automation Utilities 1.0.3 PTF UI70435 or later
* Supported by z/OS V2R3
* The z/OS® shell

.. _centralized content:
   https://ibm.github.io/z_ansible_collections_doc/index.html

.. _GitHub:
   https://github.com/ansible-collections/ibm_zos_ims

.. _Galaxy:
   https://galaxy.ansible.com/ibm/ibm_zos_ims

Version 1.0.0-beta3
====================

Notes
  * Update recommended
  * Enhancement

    * ims_acb_gen
    * ims_dbd_gen
    * ims_psb_gen
  * Documentation updates
  * Updated sample playbook

Availability
  * Galaxy
  * GitHub

Reference
  * Supported by IBM z/OS core collection v1.2.0-beta.1 or later
  * Supported by IBM Z Open Enterprise Python for z/OS: 3.8.2 or later
  * Supported by IBM Z Open Automation Utilities 1.0.3 PTF UI70435 or later
  * Supported by z/OS V2R3
  * The z/OS® shell

Version 1.0.0-beta2
====================

Notes
  * Update recommended
  * New modules

    * ims_acb_gen
  * Bug fixes
  * Documentation updates
  * Updated sample playbook

Availability
  * Galaxy
  * GitHub

Reference
  * Supported by IBM z/OS core collection 1.0.0 or later

Version 1.0.0-beta1
====================

Notes
  * Initial beta release of IBM z/OS IMS collection, referred to as ibm_zos_ims
    which is part of the broader offering
    Red Hat® Ansible Certified Content for IBM Z.
  * New modules

    * ims_dbd_gen, ims_psb_gen, ims_command

Availability
  * Galaxy
  * GitHub

