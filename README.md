# IBM® z/OS® IMS collection

The IBM z/OS IMS collection enables Ansible to interact with IBM Information Management System (IMS). The collection focuses on IMS system management operations such as generating database descriptors, program specifications, and executing IMS commands.

## Description

The **IBM z/OS IMS** collection is part of the **Red Hat® Ansible Certified Content for IBM Z®** offering that brings Ansible automation to IBM Z®. This collection enables automation of IMS tasks such as generating IMS Database Descriptors (DBD), Program Specification Blocks (PSB), Application Control Blocks (ACB), and running IMS type-1 & type-2 commands.

System programmers can automate IMS system management tasks while database administrators can streamline database operations. The collection works seamlessly with other IBM Z collections like IBM z/OS core to deliver comprehensive z/OS automation solutions.

## Requirements

This collection has been tested against the following Ansible versions: >=2.14.0,<2.17.3.

The collection requires the following on the managed node:
- IBM z/OS IMS
- IBM Open Enterprise SDK for Python
- IBM Z Open Automation Utilities (ZOAU)

> For more details about the specific versions required on the controller and managed node please visit https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/resources/releases_maintenance.html.

## Installation

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

```sh
ansible-galaxy collection install ibm.ibm_zos_ims
```

You can also include it in a requirements.yml file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
collections:
  - name: ibm.ibm_zos_ims
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the Ansible package. To upgrade the collection to the latest available version, run the following command:

```sh
ansible-galaxy collection install ibm.ibm_zos_ims --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version 1.0.0:

```sh
ansible-galaxy collection install ibm.ibm_zos_ims:1.0.0
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

## Testing

This release of the collection was tested with the following dependencies.

- ansible-core v2.17.x
- Python 3.13.x
- IBM Open Enterprise SDK for Python 3.11.x
- IBM Z Open Automation Utilities (ZOAU) 1.2.x
- z/OS V2R5

## Contributing

We welcome your contributions to improve the IBM z/OS IMS collection. Please open GitHub issues for bugs, comments, or feature requests.

## Support

As Red Hat Ansible Certified Content, this collection is entitled to support through Ansible Automation Platform (AAP). After creating a Red Hat support case, if it is determined the issue belongs to IBM, Red Hat will instruct you to create an IBM support case and share the case number with Red Hat so that a collaboration can begin between Red Hat and IBM.

## Release Notes and Roadmap

Release notes and changelogs are maintained in the [documentation](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_ims/docs/source/release_notes.html).

## Related Information

For guides and reference information, please visit:
- [IBM z/OS collections documentation](https://ibm.github.io/z_ansible_collections_doc/index.html)
- [Ansible sample playbooks using the z/OS IMS collection](https://github.com/IBM/z_ansible_collections_samples/tree/main/zos_subsystems/ims)

## License Information

© Copyright IBM Corporation 2025

This collection is licensed under [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0).
