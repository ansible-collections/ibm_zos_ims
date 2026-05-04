# IBM® z/OS® IMS collection

The IBM z/OS IMS collection enables Ansible to interact with IBM Information Management System. The collection focuses on system management operations such as generating database descriptors, program specifications, Application Control Blocks (ACB), data definition language (DDL), catalog operations, submitting DBRC commands, and executing IMS commands.

## Description

The IBM z/OS IMS collection is part of the Red Hat® Ansible Certified Content for IBM Z® offering that brings Ansible automation to IBM Z®. This collection enables automation of IMS tasks such as generating IMS Database Descriptors (DBD), Program Specification Blocks (PSB), Application Control Blocks (ACB), managing DDL, catalog operations, submitting DBRC commands, and running IMS type-1 & type-2 commands.

System programmers can automate IMS system management tasks while database administrators can streamline database operations. The collection works seamlessly with other IBM Z collections like IBM z/OS core to deliver comprehensive z/OS automation solutions.

## Requirements

This collection is tested against the following Ansible versions: 2.16.0 or later

The collection requires the following on the managed node:
- IBM z/OS IMS
- IBM Open Enterprise SDK for Python
- IBM Z Open Automation Utilities (ZOAU)

The control node requires the IBM z/OS core collection to be installed before installing the IMS collection. Refer to the [IBM z/OS Core collection requirements](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/collection-requirements.html) for specific version requirements.

## Installation

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

```sh
ansible-galaxy collection install ibm.ibm_zos_ims
```

You can also include it in a requirements.yml file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```sh
collections:
  - name: ibm.ibm_zos_ims
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the Ansible package. To upgrade the collection to the latest available version, run the following command:

```sh
ansible-galaxy collection install ibm.ibm_zos_ims --upgrade
```

You can also install a specific version of the collection, for example, if you need to install a different version. Use the following syntax to install version 1.0.0:

```sh
ansible-galaxy collection install ibm.ibm_zos_ims:1.1.0
```

You can also install a beta version of the collection. A beta version is only available on Galaxy and is only supported by the community until it is promoted to General Availability (GA). Use the following syntax to install a beta version:

```sh
ansible-galaxy collection install ibm.ibm_zos_ims:1.1.0-beta.1
```

<br/>As part of the installation, the collection [requirements](#Requirements) must be made available to Ansible through the use of environment variables. The preferred configuration is to place the environment variables in `group_vars` and `host_vars`, you can find examples of this configuration under any [playbook project](https://github.com/IBM/z_ansible_collections_samples).

<br/>If you are testing a configuration, it can be helpful to set the environment variables in a playbook, for an example to review, refer [Discussions](https://github.com/ansible-collections/ibm_zos_core/discussions/657).

<br/>To learn more about the ZOAU Python wheel installation method, review the [documentation](https://www.ibm.com/docs/en/zoau/1.3.x?topic=installing-zoau#python-wheel-installation-method).

<br/>If the wheel is installed using the `--target` option, it will install the package into the specified target directory. The environment variable `PYTHONPATH` will have to be configured to where the packages is installed, e.g; `PYTHONPATH: /usr/zoau/wheels`. Using `--target` is recommended, else the wheel will be installed in Python's home directory which may not have write permissions or persist
after an update.

<br/>If the wheel is installed using the `--user` option, it will install the package into the user directory. The environment variable `PYTHONPATH` will have to be configured to where the packages is installed, e.g; `PYTHONPATH: /u/user`.

<br/>Environment variables:

```sh
PYZ: "path_to_python_installation_on_zos_target"
ZOAU: "path_to_zoau_installation_on_zos_target"
ZOAU_PYTHON_LIBRARY_PATH: "path_to_zoau_wheel_installation_directory"

ansible_python_interpreter: "{{ PYZ }}/bin/python3"

environment_vars:
  _BPXK_AUTOCVT: "ON"
  ZOAU_HOME: "{{ ZOAU }}"
  PYTHONPATH: "{{ ZOAU_PYTHONPATH }}"
  LIBPATH: "{{ ZOAU }}/lib:{{ PYZ }}/lib:/lib:/usr/lib:."
  PATH: "{{ ZOAU }}/bin:{{ PYZ }}/bin:/bin:/var/bin"
  _CEE_RUNOPTS: "FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)"
  _TAG_REDIR_ERR: "txt"
  _TAG_REDIR_IN: "txt"
  _TAG_REDIR_OUT: "txt"
  LANG: "C"
  PYTHONSTDINENCODING: "cp1047"
```

## Use Cases

* Use Case Name: IMS Database Generation
  * Actors: Database Administrator
  * Description: A database administrator can automate the process of generating and maintaining IMS database definitions
  * Flow:
    * Generate Database Descriptor (DBD)
    * Generate Program Specification Block (PSB)
    * Generate Application Control Block (ACB)
    * Verify generation success
    * Update production libraries

* Use Case Name: IMS Command Automation
  * Actors: System Administrator
  * Description: A system administrator can automate routine IMS commands and health checks
  * Flow:
    * Execute IMS type-1 commands for system monitoring
    * Run IMS type-2 commands for advanced operations
    * Collect command responses
    * Process and analyze results
    * Generate operational reports

* Use Case Name: IMS System Maintenance
  * Actors: System Programmer
  * Description: A system programmer can automate IMS maintenance procedures
  * Flow:
    * Verify system status
    * Back up critical resources
    * Apply maintenance
    * Validate changes
    * Generate maintenance report

* Use Case Name: IMS Catalog Population
  * Actors: Database Administrator
  * Description: A database administrator can automate the population and maintenance of the IMS catalog
  * Flow:
    * Prepare catalog datasets
    * Use DDL to define database structures
    * Populate catalog with database metadata
    * Verify catalog entries
    * Update catalog documentation

* Use Case Name: IMS Database Recovery Control
  * Actors: System Administrator
  * Description: A system administrator can automate DBRC operations for database recovery and backup management
  * Flow:
    * Submit DBRC commands for database registration
    * Monitor backup status through DBRC queries
    * Automate recovery scenarios
    * Manage RECON datasets
    * Generate DBRC reports

## Testing

All releases will meet the following test criteria.

* 100% success for [Functional](https://github.com/ansible-collections/ibm_zos_ims/tree/dev/tests/functional) tests.
* 100% success for [Unit](https://github.com/ansible-collections/ibm_zos_ims/tree/dev/tests/units) tests.
* 100% success for [Sanity](https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/index.html#all-sanity-tests) tests as part of [ansible-test](https://docs.ansible.com/ansible/latest/dev_guide/testing.html#run-sanity-tests).
* 100% success for [ansible-lint](https://ansible.readthedocs.io/projects/lint/) allowing only false.

This release of the collection was tested with the following dependencies.

- ansible-core v2.16.x
- Python 3.13.x
- IBM Open Enterprise SDK for Python 3.12.x
- IBM Z Open Automation Utilities (ZOAU) 1.3.x
- z/OS V2R5 or later

## Contributing

This community is not currently accepting contributions. However, we encourage you to open git issues for bugs, comments or feature requests.

Review this content periodically to learn when and how to make contributions in the future. For the latest information on open issues, see: [git issues](https://github.com/ansible-collections/ibm_zos_ims/issues).

## Communication

If you would like to communicate with this community, you can do so through the following options.

* GitHub [discussions](https://github.com/ansible-collections/ibm_zos_ims/discussions).
* GitHub [issues](https://github.com/ansible-collections/ibm_zos_ims/issues/new/choose).
* [Ansible Forum](https://forum.ansible.com/), please use the `zos` tag to ensure proper awareness.
* Discord [System Z Enthusiasts](https://discord.gg/sze) room `ansible`.
* Matrix general usage questions [room](https://matrix.to/#/#users:ansible.com).

## Support

As Red Hat Ansible [Certified Content](https://catalog.redhat.com/software/search?target_platforms=Red%20Hat%20Ansible%20Automation%20Platform), this collection is entitled to [support](https://access.redhat.com/support/) through [Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible) (AAP). After creating a Red Hat support case, if it is determined the issue belongs to IBM, Red Hat will instruct you to create an [IBM support case](https://www.ibm.com/mysupport/s/createrecord/NewCase) and share the case number with Red Hat so that a collaboration can begin between Red Hat and IBM.

<br/>If a support case cannot be opened with Red Hat and the collection has been obtained either from [Galaxy](https://galaxy.ansible.com/ui/) or [GitHub](https://github.com/ansible-collections/ibm_zos_ims), there is community support available at no charge. Community support is limited to the collection; community support does not include any of the Ansible Automation Platform components, [IBM Z Open Automation Utilities](https://www.ibm.com/docs/en/zoau), [IBM Open Enterprise SDK for Python](https://www.ibm.com/products/open-enterprise-python-zos).

<br/>The current supported versions of this collection can be found listed under the [release section](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_ims/docs/source/release_notes.html).

## Release Notes and Roadmap

For the collection's cumulative, refer [release notes](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_ims/docs/source/release_notes.html) are an easy way to review changes. The collection [Life Cycle](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_ims/docs/source/life-cycle_ims.html) also referred to as the Roadmap contains changelog details, support dates and the current level of support
for each collection. For a complete guide to support, review the **Ansible for IBM Z** [Collection Life Cycles](https://ibm.github.io/z_ansible_collections_doc/collections_content/collection-life-cycles.html#life-cycles).

## Related Information

Example playbooks and use cases can be be found in the [Ansible sample playbooks using the z/OS IMS collection](https://github.com/IBM/z_ansible_collections_samples/tree/main/zos_subsystems/ims). For supplemental content on getting started with Ansible, architecture and use cases, refer to [IBM z/OS collections documentation](https://ibm.github.io/z_ansible_collections_doc/index.html).

## License Information

Some portions of this collection are licensed under [GNU General Public License, Version 3.0](https://opensource.org/licenses/GPL-3.0), and other portions of this collection are licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
See individual files for applicable licenses.
