.. ...........................................................................
.. © Copyright IBM Corporation 2020                                          .
.. ...........................................................................

Managed node
============

The managed z/OS node is the host that is managed by Ansible, as identified in
the Ansible inventory. The managed node has dependencies that are specific
to each release of the **IBM z/OS IMS collection**. Review the details of the
dependencies before you proceed to install the IBM z/OS IMS collection.

* `IBM Open Enterprise Python for z/OS`_
* `z/OS`_ V2R5 - V3Rx
* `IBM Z Open Automation Utilities`_ (ZOAU)

  * IBM z/OS IMS collections are dependent on specific versions of ZOAU.
    For information about the required version of ZOAU, review the
    `release notes`_.

* `z/OS OpenSSH`_
* The z/OS shell
* `IBM IMS V15 or later`_

.. note::

   Only the `z/OS shell`_ is supported, using ``ansible_shell_executable``
   to change the default shell is unsupported. Other shells are not supported
   because they handle the reading and writing of untagged files differently.

.. _Ansible documentation:
   https://docs.ansible.com/ansible/2.7/user_guide/intro_inventory.html

.. _z/OS:
   https://www.ibm.com/docs/en/zos

.. _IBM Z Open Automation Utilities:
   requirements_managed.html#zoau

.. _z/OS OpenSSH:
   https://www.ibm.com/support/knowledgecenter/SSLTBW_2.2.0/com.ibm.zos.v2r2.e0za100/ch1openssh.htm

.. _IBM IMS V15 or later:
   https://www.ibm.com/support/knowledgecenter/SSEPH2_15.1.0/com.ibm.ims15.doc/ims_product_landing_v15.html

.. _release notes:
   release_notes.html

.. _z/OS shell:
   https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.4.0/com.ibm.zos.v2r4.bpxa400/part1.htm

Python on z/OS
--------------

If the Ansible target is z/OS, you must install
**IBM Open Enterprise Python for z/OS** which is ported for the z/OS platform
and required by **IBM z/OS IMS Collection**.

**Installation**

* Visit the `IBM Open Enterprise Python for z/OS`_ product page for FMID,
  program directory, fix list, latest PTF, installation and configuration
  instructions.
* For reference, the Program IDs are:

  * 5655-PYT for the base product
  * 5655-PYS for service and support
* Optionally download **IBM Open Enterprise Python for z/OS**, `here`_
* For the Python supported version, refer to the `release notes`_.

.. _IBM Open Enterprise Python for z/OS:
   http://www.ibm.com/products/open-enterprise-python-zos

.. _here:
   https://www-01.ibm.com/marketing/iwm/platform/mrs/assets?source=swg-ibmoep

.. note::

   Currently, IBM Open Enterprise Python for z/OS is the supported and
   recommended Python distribution for use on z/OS with Ansible and ZOAU.

ZOAU
----

IBM Z Open Automation Utilities provide support for executing automation tasks
on z/OS. With ZOAU, you can run traditional MVS commands, such as IEBCOPY,
IDCAMS, and IKJEFT01, as well as perform a number of data set operations
in the scripting language of your choice.

**Installation**

* Visit the `ZOAU`_ product page for the FMID, program directory, fix list,
  latest PTF, installation and configuration instructions.
* For reference, the Program IDs are:

  * 5698-PA1 for the base product
  * 5698-PAS for service and support
* For ZOAU supported version, refer to the `release notes`_.

.. _ZOAU:
   https://www.ibm.com/support/knowledgecenter/en/SSKFYE

