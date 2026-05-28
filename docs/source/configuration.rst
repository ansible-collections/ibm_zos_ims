.. ...........................................................................
.. © Copyright IBM Corporation 2026
..
.. This is an orphaned page because its not included in any toctree
.. 'orphan' if set, warnings about this file not being included in any toctree
..  will be suppressed.
.. ...........................................................................

:orphan:

=============
Configuration
=============

After you install the IBM z/OS core collection, configure the files 
so the collection can locate the dependencies required to run the modules on the managed node.

Step 1: Directory Structure
===========================

.. dropdown:: The following section discusses configuring the collection ... (expand for more)
    :color: primary
    :icon: info

    1. Create a directory structure that includes the playbooks, inventory, 
    variables (group_vars and host_vars), and environment variables.

    In this example, we use an alternative directory layout that places the 
    inventory together with group_vars and host_vars. This layout is especially useful 
    when the variables in group_vars and host_vars differ significantly from those used 
    by other systems (e.g., Linux, Windows).

    This directory structure complete with playbook and configurations is
    available in `Ansible Z Playbook Repository`_.

    Create the directory structure on the control node—the machine where Ansible runs.

    .. code-block:: sh

        /playbooks/
                ├── my_playbook.yml       # A playbook
                ├── another_playbook.yml  # Another playbook
                ├── ansible.cfg           # Custom Ansible configuration
                ├── inventories/
                    └── host_vars/        # Assign variables to particular systems
                        └── zos_host.yml
                    └── group_vars/       # Assign variables to particular groups
                        └── all.yml
                    └── inventory.yml     # Inventory file for production systems


    The following commands creates this directory structure in the `/tmp`
    directory.

    .. code-block:: sh

        mkdir -p /tmp/playbooks;
        touch /tmp/playbooks/my_playbook.yml;
        touch /tmp/playbooks/another_playbook.yml;
        touch /tmp/playbooks/ansible.cfg;
        mkdir -p /tmp/playbooks/inventories;
        mkdir -p /tmp/playbooks/inventories/host_vars;
        touch /tmp/playbooks/inventories/host_vars/zos_host.yml;
        mkdir -p /tmp/playbooks/inventories/group_vars;
        touch /tmp/playbooks/inventories/group_vars/all.yml;
        touch /tmp/playbooks/inventories/inventory.yml;


Step 2: Host variables (host_vars)
==================================

.. dropdown:: The following section discusses *host_vars* ... (expand for more)
    :color: primary
    :icon: file-code

    This section describes the host_vars files. Ansible expands them automatically into environment 
    variables that tell the collection where to find the required dependencies:
    - IBM `Open Enterprise SDK for Python`_ 
    - IBM `Z Open Automation Utilities`_ (ZOAU) dependencies.

    These variables enable the collection to locate the SDK and ZOAU on the managed node.

    If you have not installed either dependency, Review the
    `managed node requirements`_ for this collection.

    Before you continue, gather the following information:

        #. The absolute path of where **IBM Open Enterprise SDK for Python** is installed.
        #. The IBM Open Enterprise SDK for Python **version** installed, eg v3.12.
        #. The absolute path of where **Z Open Automation Utilities** (ZOAU) is installed.
        #. The absolute path of **ZOAU python package** (zoautil-py) which can vary
           depending if ``pip3`` was used to install the python package.

            - If ``pip3`` was **not** used to install the ZOAU python package, you can find
              the compiled package under **<path to zoau>/lib/<python version>**, for
              example **/usr/lpp/IBM/zoautil/1.12**.
            - If ``pip3`` was used to install the ZOAU python package, the following command
              can aid in finding the absolute path to the package.

                .. code-block:: sh

                    pip3 show zoautil-py

            This results in showing the '**Location**' of the package, for example:

            .. code-block:: sh

                Name: zoautil-py
                Version: 1.3.0.1
                Summary: Automation utilities for z/OS
                Home-page: https://www.ibm.com/docs/en/zoau/latest
                Author: IBM
                Author-email: csosoft@us.ibm.com
                Location: /zstack/zpm/python/3.10.0.0/lib/python3.10/site-packages

    Now that you have gathered the required dependency details, edit the file
    ``zos_host.yml`` located at ``/tmp/playbooks/inventories/host_vars/zos_host.yml``
    that was created in '**Step 1: Directory Structure**'.

    .. dropdown:: You need to configure the following properties ... (expand for more)
        :color: info
        :icon: file-code

        You need to configure the following properties.

        PYZ
            - The python installation home path on the z/OS manage node.
        PYZ_VERSION
            - The version of python on the z/OS managed node.
        ZOAU
            - The ZOAU installation home on the z/OS managed node.
        ZOAU_PYTHON_LIBRARY_PATH
            - The path to the ZOAU python library 'zoautil_py'.

    .. dropdown:: If you have installed the ZOAU python package using *pip3* ... (expand for more)
        :color: info
        :icon: file-code

        If you have installed the ZOAU python package using ``pip3``, enter this into
        ``zos_host.yml`` and update only the environment variables `PYZ`, `PYZ_VERSION`,
        `ZOAU`, `ZOAU_PYTHON_LIBRARY_PATH` with the dependency paths.

        .. code-block:: sh

            PYZ: "/usr/lpp/IBM/cyp/v3r12/pyz"
            PYZ_VERSION: "3.12"
            ZOAU: "/usr/lpp/IBM/zoautil"
            ZOAU_PYTHON_LIBRARY_PATH: "/usr/lpp/IBM/cyp/v3r12/pyz/lib/python3.12/site-packages/"
            ansible_python_interpreter: "{{ PYZ }}/bin/python3"

    .. dropdown:: If you are using the included pre-compiled ZOAU python binaries ... (expand for more)
        :color: info
        :icon: file-code

        If you are using the included pre-compiled ZOAU python binaries, enter this
        into ``zos_host.yml``` and update only the environment variables
        `PYZ`, `PYZ_VERSION`, `ZOAU` with the dependency paths.

        .. code-block:: sh

            PYZ: "/usr/lpp/IBM/cyp/v3r12/pyz"
            PYZ_VERSION: "3.12"
            ZOAU: "/usr/lpp/IBM/zoautil"
            ZOAU_PYTHON_LIBRARY_PATH: "{{ ZOAU }}/lib/{{ PYZ_VERSION }}"
            ansible_python_interpreter: "{{ PYZ }}/bin/python3"


    .. admonition:: Use environment variables in a playbook

        If you are testing a configuration, set the environment variables
        in a playbook. For this option, see: `How to put environment variables in a playbook`_.

Step 3: Group variables (group_vars)
====================================

.. dropdown:: The following section discusses *group_vars* ... (expand for more)
    :color: primary
    :icon: file-code

    The following section discusses ``group_vars``, part of the
    environment variables which instructs the location of the collection
    IBM `Open Enterprise SDK for Python`_ and IBM
    `Z Open Automation Utilities`_ (ZOAU) dependencies.

    In the ``all.yml`` file located at ``/tmp/playbooks/inventories/group_vars/all.yml``,
    paste the following below, there is no need to edit this content. The ``host_vars``
    variables from the previous is substituted automatically into the
    environment variables (below) by ansible.

    Notice the indentation, ensure it is retained before you save the file.

    .. code-block:: sh

        environment_vars:
          _BPXK_AUTOCVT: "ON"
          ZOAU_HOME: "{{ ZOAU }}"
          PYTHONPATH: "{{ ZOAU_PYTHON_LIBRARY_PATH }}"
          LIBPATH: "{{ ZOAU }}/lib:{{ PYZ }}/lib:/lib:/usr/lib:."
          PATH: "{{ ZOAU }}/bin:{{ PYZ }}/bin:/bin:/var/bin"
          _CEE_RUNOPTS: "FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)"
          _TAG_REDIR_ERR: "txt"
          _TAG_REDIR_IN: "txt"
          _TAG_REDIR_OUT: "txt"
          LANG: "C"
          PYTHONSTDINENCODING: "cp1047"


    .. dropdown:: The following section explains the environment variables ... (expand for more)
        :color: info
        :icon: file-code

        The following section explains the environment variables.

        BPXK_AUTOCVT
            - Activate automatic file conversion of tagged files
              including I/O for regular, pipe, and character-special files that are tagged.
        ZOAU_HOME
            - the Z Open Automation Utilities (ZOAU) install root path.
        PYTHONPATH
            - The ZOAU Python library path.
        LIBPATH
            - The Python libraries  path on the managed node and the ZOAU python
              library path separated by semi-colons.
        PATH
            - The ZOAU `/bin` path and Python interpreter path.
        _CEE_RUNOPTS
            - The invocation Language Environment runtime options for programs.
        _TAG_REDIR_IN
            - Enables tagging of the shell's stdin redirection based on the
              existing file tags. It must be set to txt.
        _TAG_REDIR_OUT
            - Enables tagging of the shell's stdout redirection based on the
              existing file tags. It must be set to txt.
        _TAG_REDIR_ERR
            - enables tagging of the shell's stderr redirection based on the
              existing file tags. It must be set to txt.
        LANG
            - The name of the default locale. The C value specifies the Portable Operating
              System Interface (POSIX) locale.
        PYTHONSTDINENCODING
            - Instructs Ansible which encoding it will pipe content to Python's stdin
              when ``pipelining=true`` the encoding Unix System Services is configured as,
              supported encodings are ASCII or EBCDIC.

Step 4: Inventory
==================

.. dropdown:: The following section discusses how Ansible interacts with managed node ... (expand for more)
    :color: primary
    :icon: file-code

    The following section discusses how Ansible interacts with managed
    nodes (hosts) using a list known as `inventory`_. It is a configuration file that
    specifies the hosts and group of hosts on which Ansible commands, modules, and playbooks
    will operate. It also defines variables and connection details for those hosts, such as
    IP address. For more information, see `Building Ansible inventories`_.

    The following inventory is explained.

    - **systems** is a group that contains one managed host, **zos1**.
    - **zos1** is the name chosen for managed node, you can choose any name. 
    - **ansible_host** is an ansible reserved keyword that is the hostname ansible
      connects to and run automated tasks on, it can be an LPAR, ZVM, etc.
    - **ansible_user** is an ansible reserved keyword that is the user Ansible
      uses to connect to the managed node, generally and OMVS segment.

    Edit the file ``inventory.yml`` located at ``/tmp/playbooks/inventories/inventory.yml``
    and paste the following below. You need to update the properties
    **ansible_host** and **ansible_user**.

    .. code-block:: sh

        systems:
            hosts:
                zos1:
                ansible_host: zos_managed_node_host_name_or_ip
                ansible_user: zos_managed_node_ssh_user

Step 5: User
============

.. dropdown:: The following section discusses how the collection connects to the managed node over SSH ... (expand for more)
    :color: primary
    :icon: command-palette

    The following section discusses how the collection connects to the
    managed node over SSH via the ansible user defined in inventory or optionally
    the command line, thus requiring access to z/OS UNIX System Services (USS).
    From a security perspective, the collection will require both an OMVS segment
    and TSO segment in the users profile.

    With the RACF **ADDGROUP** command you can:

    - Define a new group to RACF.
    - Add a profile for the new group to the RACF database.
    - Specify z/OS UNIX System Services information for the group being defined to RACF.
    - specify that RACF is to automatically assign an unused GID value to the group.

    With the RACF **ADDUSER** command you can:

    - Define a new user to RACF.
    - Add a profile for the new user to the RACF database.
    - Create a connect profile that connects the user to the default group.
    - Create an OMVS segment.
    - Create a TSO segment.

    When issuing RACF commands, you might require sufficient authority to the proper
    resources. It is recommended you review the `RACF language reference`_.

    You can define a new group to RACF with command:

    .. code-block:: sh

       ADDGROUP gggggggg OMVS(AUTOGID)

    You can add a new user with RACF command:

    .. code-block:: sh

       ADDUSER uuuuuuuu DFLTGRP(gggggggg) OWNER(nnnnnnnn) PASSWORD(pppppppp) TSO(ACCTNUM(aaaaaaaa) PROC(pppppppp)) OMVS(HOME(/u/uuuuuuuu) PROGRAM('/bin/sh')) AUTOUID

    To learn more about creating users with RACF, see `RACF command syntax`_.

    .. dropdown:: The following section explains the RACF operands ... (expand for more)
        :color: info
        :icon: file-code

        The following section explains the RACF operands used in the above RACF commands.

        uuuuuuuu
            - Specifies the user to be defined to RACF. 1 - 8 alphanumeric characters. A
              user id can contain any of the supported symbols A-Z, 0-9, #, $, or @.
        gggggggg
            - Specifies the name of a RACF-defined group to be used as the default
              group for the user. If you do not specify a group, RACF uses your current connect
              group as the default. 1 - 8 alphanumeric characters, beginning with an alphabetic
              character. A group name can contain any of the supported symbols A-Z, 0-9, #, $, or @.
        nnnnnnnn
            - Specifies a RACF-defined user or group to be assigned as the owner of the
              new group. If you do not specify an owner, you are defined as the owner of the group.
        pppppppp
            - Specifies the user's initial logon password. This password is always set
              expired, thus requiring the user to change the password at initial logon.
        aaaaaaaa
            - Specifies the user's default TSO account number. The account number you
              specify must be protected by a profile in the ACCTNUM general resource class, and
              the user must be granted READ access to the profile.

Step 6: Run a playbook
======================

.. dropdown:: The following section discusses how to run an Ansible playbook ... (expand for more)
    :color: primary
    :icon: command-palette

    The following section discusses how to use the IBM z/OS IMS collection in an Ansible playbook.
    An `Ansible playbook`_ consists of organized instructions that define work for a managed
    node (host) to be managed with Ansible.

    After completing steps 1–5, you are ready to run a playbook. The following example demonstrates
    a simple Type-2 command that queries all programs for IMS1 in PLEX1 by using the
    `ibm_zos_ims.ims_command`_ module. The module processes the command and returns the corresponding program details for PLEX1.

    .. code-block:: sh

        ---
        - hosts: all
          collections:
            - ibm.ibm_zos_ims
            - ibm.ibm_zos_core
          environment: "{{ environment_vars }}"

          tasks:
            - name: IMS command - query all programs for IMS1 in PLEX1
              ims_command:
                command: QUERY PGM SHOW(ALL)
                plex: PLEX1
                route: IMS1
              register: result
              
            - name: Display all IMS programs for IMS1 in PLEX1
               debug:
                 msg: "{{result}}"


    Copy the above playbook into a file, call it **sample.yml** and to run it,
    use the Ansible command ``ansible-playbook`` with the inventory you defined
    in step 4 along with a reqeust for a password using opiton ``--ask-pass``.

    The command syntax is ``ansible-playbook -i <inventory> <playbook> --ask-pass``,
    for example;

    .. code-block:: sh

        ansible-playbook -i inventory sample.yaml

    You can avoid a password prompt by configuring SSH keys, see `setting up SSH keys`_.

    For further reading, review `run your first command and playbook`_ and follow up
    with `Ansible playbooks`_.


    .. dropdown:: Optionally, you can configure the console logging verbosity ... (expand for more)
        :color: success
        :icon: info

        Optionally, you can configure the console logging verbosity during playbook
        execution. This is helpful in situations where communication is failing and
        you want to obtain more details. To adjust the logging verbosity, append more
        letter ``v``'s; for example, ``-v``, ``-vv``, ``-vvv``, or ``-vvvv``. Each letter
        ``v`` increases logging verbosity similar to traditional logging levels **INFO**,
        **WARN**, **ERROR**, **DEBUG**.

        Using the previous example, the following sets the highest level of
        verbosity.

        .. code-block:: sh

            ansible-playbook -i inventory sample.yaml -vvvv

.. ...........................................................................
.. External links
.. ...........................................................................
.. _Ansible Z Playbook Repository:
   https://github.com/IBM/z_ansible_collections_samples
.. _How to put environment variables in a playbook:
   https://github.com/ansible-collections/ibm_zos_core/discussions/657
.. _Open Enterprise SDK for Python:
   https://www.ibm.com/products/open-enterprise-python-zos
.. _Z Open Automation Utilities:
   https://www.ibm.com/docs/en/zoau/latest
.. _RACF command syntax:
   https://www.ibm.com/docs/en/zos/3.1.0?topic=syntax-addgroup-add-group-profile
.. _RACF language reference:
   https://www.ibm.com/docs/en/zos/3.1.0?topic=racf-zos-security-server-command-language-reference
.. _inventory:
   https://docs.ansible.com/projects/ansible/latest/getting_started/basic_concepts.html#inventory
.. _Building Ansible inventories:
   https://docs.ansible.com/ansible/latest/inventory_guide/index.html#
.. _Ansible playbook:
   https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#playbooks-intro
.. _ibm_zos_ims.ims_command:
    https://ibm.github.io/z_ansible_collections_doc/ibm_zos_ims/docs/source/modules/ims_command.html
.. _setting up SSH keys:
   https://docs.ansible.com/ansible/latest/inventory_guide/connection_details.html#setting-up-ssh-keys
.. _Ansible playbooks:
   https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#about-playbooks
.. _run your first command and playbook:
   https://docs.ansible.com/ansible/latest/network/getting_started/first_playbook.html#run-your-first-command-and-playbook
.. _managed node requirements:
   collection-requirements.html#control-node
