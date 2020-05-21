.. ...........................................................................
.. © Copyright IBM Corporation 2020                                          .
.. ...........................................................................

Playbooks
=========

The sample playbooks that are **included** in the **IBM z/OS IMS collection**
demonstrate how to use the collection content.

Playbook Documentation
----------------------

An `Ansible playbook`_ consists of organized instructions that define work for
a managed node (host) to be managed with Ansible.

A `playbooks directory`_ that contains a sample playbook is included in the
**IBM z/OS IMS collection**. The sample playbook is for reference and can be run
with the ``ansible-playbook`` command with some modification to the **inventory**,
**ansible.cfg** and **group_vars** as well as updates to the module parameters
to reference your IMS artifacts and configuration.

To get started with configuring your environment for running playbooks, see the
`sample configuration and setup`_ section and the `sample playbooks`_ in the
**IBM z/OS core collection.**

You can find the playbook content that is included with the collection in the
same location where the collection is installed. For more information, refer to
the `installation documentation`_. 

The sample playbook that is included in the **IBM z/OS IMS collection** demonstrates
how to perform tasks using the modules included in the **Red Hat Ansible Certified
Content for IBM z/OS IMS collection.** The sample does not demonstrate all of the
available module options for the collection. To learn more about all the available
options, refer to the ansible-doc or the `module reference`_.

.. _Ansible playbook:
   https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#playbooks-intro
.. _playbooks directory:
   https://github.com/ansible-collections/ibm_zos_ims/tree/master/playbooks
.. _sample configuration and setup:
   https://ansible-collections.github.io/ibm_zos_core/playbooks.html#sample-configuration-and-setup
.. _sample playbooks:
   https://github.com/ansible-collections/ibm_zos_core/tree/master/playbooks
.. _installation documentation:
   installation.html
.. _module reference:
   modules.html