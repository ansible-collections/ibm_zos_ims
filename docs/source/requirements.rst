.. ...........................................................................
.. © Copyright IBM Corporation 2026                                          .
.. ...........................................................................

============
Requirements
============

The **IBM z/OS IMS collection** requires both a **control node** and
**managed node** be configured with a minimum set of requirements. The
control node is often referred to as the **controller** and the
managed node as the **host** or **target**.

Control node
============
The controller is where the Ansible engine that runs the playbook is installed.
For more information on the `controllers dependencies`_, refer to RedHat Ansible 
Certified Content documentation .

.. _controllers dependencies:
   https://ibm.github.io/z_ansible_collections_doc/requirements/requirements_controller.html


.. toctree::
   :maxdepth: 3

   requirements_managed

