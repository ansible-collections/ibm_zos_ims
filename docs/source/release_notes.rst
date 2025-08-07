.. ...........................................................................
.. © Copyright IBM Corporation 2025                                          .
.. ...........................................................................

========
Releases
========

Version 1.3.1
====================

Notes
-----

 * Compatability to the latest dependencies versions 

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
* Supported by IBM Z Open Automation Utilities (ZOAU) through v1.3.0 or later.

  *  ZOAU minimum supported version may vary depending on the z/OS core collection version that is chosen. For details on z/OS core collection requirements, see `release-v1.15.0-beta.1`_.
* Supported by z/OS V2R4 (or later)
* The z/OS® shell

.. _centralized content:
   https://ibm.github.io/z_ansible_collections_doc/index.html

.. _GitHub:
   https://github.com/ansible-collections/ibm_zos_ims

.. _Galaxy:
   https://galaxy.ansible.com/ibm/ibm_zos_ims

.. _release-v1.15.0-beta.1:
   https://github.com/ansible-collections/ibm_zos_core/releases

Version 1.3.0
====================

Notes
-----

* Update recommended

  * type() was replaced by isinstance() in the code for gen utilities since ansible-core 2.16 supports Python 3.12 and that version deprecated type() function. 
  * No other changes from version 1.3.0-beta.1 release. Collection promoted to certified content with version 1.3.0.

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

  * ZOAU minimum supported version may vary depending on the z/OS core collection version that is chosen. For details on z/OS core collection requirements, see `release-v1.15.0-beta.1`_.
* Supported by z/OS V2R4 (or later) but prior to version V3R1.
* The z/OS® shell.

.. _centralized content:
   https://ibm.github.io/z_ansible_collections_doc/index.html

.. _GitHub:
   https://github.com/ansible-collections/ibm_zos_ims

.. _Galaxy:
   https://galaxy.ansible.com/ibm/ibm_zos_ims
    
.. _release-v1.15.0-beta.1:
   https://github.com/ansible-collections/ibm_zos_core/releases

