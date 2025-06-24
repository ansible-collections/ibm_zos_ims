IBM z/OS IMS collection
========================

The **IBM z/OS IMS collection**, also represented as **ibm\_zos\_ims**
in this document, is part of the broader offering **Red Hat® Ansible
Certified Content for IBM Z**. The IBM z/OS IMS collection supports tasks
such as generating IMS Database Descriptors (DBD), Program 
Specification Blocks (PSB), Application Control Blocks (ACB), and 
running IMS type-1 & type-2 commands.  

The **IBM z/OS IMS collection** works closely with offerings such as the 
[IBM z/OS core collection](https://github.com/ansible-collections/ibm_zos_core) 
to deliver a solution that will enable you to automate tasks on z/OS.

Red Hat Ansible Certified Content for IBM Z
===========================================

**Red Hat® Ansible Certified Content for IBM Z** provides the ability to
connect IBM Z® to clients\' wider enterprise automation strategy through
the Ansible Automation Platform ecosystem. This enables development and
operations automation on Z through a seamless, unified workflow
orchestration with configuration management, provisioning, and
application deployment in one easy-to-use platform.

**The IBM z/OS IMS collection**, as part of the broader offering
**Red Hat® Ansible Certified Content for IBM Z**, is available on Galaxy as 
community supported.

<<<<<<< Updated upstream
For **guides** and **reference**, please visit [the documentation
site](https://ibm.github.io/z_ansible_collections_doc/index.html).
=======
This collection is tested against the following Ansible versions: >=2.14.0,<2.17.3.
>>>>>>> Stashed changes

Features
========

<<<<<<< Updated upstream
The IBM IMS collection includes
[modules](https://github.com/ansible-collections/ibm_zos_ims/tree/master/plugins/modules/),
and ansible-doc to automate tasks on IMS.
=======
Before you install the IMS collection, the control node requires installation of the IBM z/OS core collection. Refer to the [IBM z/OS collections support matrix](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/resources/releases_maintenance.html#support-matrix) for specific version requirements.
>>>>>>> Stashed changes


Ansible version compatibility
==============================

This collection has been tested against the following Ansible versions: >=2.14.0,<2.17.0.

<<<<<<< Updated upstream
=======
You can include it in a requirements.yml file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
>>>>>>> Stashed changes

Copyright
=========

<<<<<<< Updated upstream
© Copyright IBM Corporation 2020

License
=======
=======
Note that if you install the collection from Ansible Galaxy, it is not upgraded automatically when you upgrade the Ansible package. To upgrade the collection to the latest available version, run the following command:

```sh
ansible-galaxy collection install ibm.ibm_zos_ims --upgrade
```

You can install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (report an issue in this repository). Use the following syntax to install version 1.2.0:

```sh
ansible-galaxy collection install ibm.ibm_zos_ims:1.2.0
```

## Use Cases

* Use Case Name: IMS Database Generation
  * Actors: Database Administrator
  * Description: A database administrator can automate the process of generating and maintaining IMS database definitions.
  * Flow:
    * Generate Database Descriptor (DBD)
    * Generate Program Specification Block (PSB)
    * Generate Application Control Block (ACB)
    * Verify generation success
    * Update production libraries

* Use Case Name: IMS Command Automation
  * Actors: System Administrator
  * Description: A system administrator can automate routine IMS commands and health checks.
  * Flow:
    * Execute IMS type-1 commands for system monitoring
    * Run IMS type-2 commands for advanced operations
    * Collect command responses
    * Process and analyze results
    * Generate operational reports

* Use Case Name: IMS System Maintenance
  * Actors: System Programmer
  * Description: A system programmer can automate IMS maintenance procedures.
  * Flow:
    * Verify system status
    * Back up critical resources
    * Apply maintenance
    * Validate changes
    * Generate maintenance report

* Use Case Name: IMS Catalog Population
  * Actors: Database Administrator
  * Description: A database administrator can automate the population and maintenance of the IMS catalog.
  * Flow:
    * Prepare catalog datasets
    * Use DDL to define database structures
    * Populate catalog with database metadata
    * Verify catalog entries
    * Update catalog documentation

* Use Case Name: IMS Database Recovery Control
  * Actors: System Administrator
  * Description: A system administrator can automate DBRC operations for database recovery and backup management.
  * Flow:
    * Submit DBRC commands for database registration
    * Monitor backup status through DBRC queries
    * Automate recovery scenarios
    * Manage RECON datasets
    * Generate DBRC reports

## Testing

This release of the collection was tested with the following dependencies.

- ansible-core v2.17.x
- Python 3.13.x
- IBM Open Enterprise SDK for Python 3.11.x
- IBM Z Open Automation Utilities (ZOAU) 1.2.x
- z/OS V2R5

## Contributing

We are not currently accepting community contributions. However, we encourage you to open git issues for bugs, comments or feature requests.

Review this content periodically to learn when and how to make contributions in the future. For the latest information on open issues, see: [git issues](https://github.com/ansible-collections/ibm_zos_ims/issues).

## Support

As Red Hat Ansible Certified Content, this collection is entitled to support through Ansible Automation Platform (AAP). After you create a Red Hat support case, if it is determined the issue belongs to IBM, Red Hat instructs you to create an IBM support case and share the case number with Red Hat so that a collaboration can begin between Red Hat and IBM.

## Release Notes and Roadmap

Release notes and changelogs are maintained in the [documentation](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_ims/docs/source/release_notes.html).

## Related Information

For guides and reference information, refer to:
- [IBM z/OS collections documentation](https://ibm.github.io/z_ansible_collections_doc/index.html)
- [Ansible sample playbooks using the z/OS IMS collection](https://github.com/IBM/z_ansible_collections_samples/tree/main/zos_subsystems/ims)

## License Information

© Copyright IBM Corporation 2025
>>>>>>> Stashed changes

This collection is licensed under [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0).

