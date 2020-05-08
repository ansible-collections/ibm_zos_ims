# z/OS Ansible Module Testing

This document outlines processes to run and develop test cases for z/OS Ansible modules.

- [z/OS Ansible Module Testing](#zos-ansible-module-testing)
  - [Prerequisites](#prerequisites)
    - [Control Node](#control-node)
    - [z/OS Target Host](#zos-target-host)
  - [Running Test Cases](#running-test-cases)
    - [Install Requirements](#install-requirements)
    - [SSH Keys](#ssh-keys)
      - [Generate and add new SSH key](#generate-and-add-new-ssh-key)
      - [Copy public key to target host](#copy-public-key-to-target-host)
    - [Run All Tests](#run-all-tests)
    - [Run Unit Tests](#run-unit-tests)
    - [Run Functional Tests](#run-functional-tests)
    - [Configuration and Arguments](#configuration-and-arguments)
      - [YAML Arguments](#yaml-arguments)
      - [CLI Arguments](#cli-arguments)
      - [Add module directory to ANSIBLE_LIBRARY](#add-module-directory-to-ansiblelibrary)
  - [Running Test Cases Using Bash Script](#running-test-cases-using-bash-script)

## Prerequisites

### Control Node

* Preferably latest Python 3.X
* Up to date Ansible, 2.8 confirmed working

### z/OS Target Host

* [Z Open Automation Utilities](https://www.ibm.com/support/knowledgecenter/en/SSKFYE_1.0.0/zoautil_overview.html)
* Python 3 >= 3.6

## Running Test Cases

### Install Requirements

From root of collection:

```bash
pip3 install -r tests/requirements.txt
```

If the above command responds with: `ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied`

```bash
pip3 install --user -r tests/requirements.txt
```

### SSH Keys

#### Generate and add new SSH key

Using [ssh-keygen](https://www.ssh.com/ssh/keygen/) and [ssh-add](https://www.ssh.com/ssh/add)

![addkey](https://zenhub.ibm.com/images/5c75c71e85b6d5070636e1d8/8bd18b60-7517-4301-b3d4-17857e3a5e49)

#### Copy public key to target host

Using [ssh-copy-id](https://www.ssh.com/ssh/copy-id)

![sshcopyid](https://zenhub.ibm.com/images/5c75c71e85b6d5070636e1d8/63102702-1dd4-4578-8539-33beb496bf69)

### Run All Tests

First, complete the [functional test configuration steps](#run-functional-tests).

__If Python 2 is default__

Assuming the absolute path of the YAML configuration file is `/home/myuser/test_config.yml`

```bash
python3 -m pytest --host-pattern=all --zinventory=/home/myuser/test_config.yml
```

__If Python 3 is default__

Assuming the absolute path of the YAML configuration file is `/home/myuser/test_config.yml`

```bash
pytest --host-pattern=all --zinventory=/home/myuser/test_config.yml
```

By default, `--zinventory` (or `-Z` ) is set to `test_config.yml` in the working directory.

### Run Unit Tests

The unit tests should not require access to a z/OS system to run and require minimal configuration to get started.

__Navigate to the unit tests folder__

```
ansible_collections_ibm_zos_core
└── tests
    └── units
```

__If Python 2 is default__

```bash
python3 -m pytest
```

__If Python 3 is default__

```bash
pytest
```

### Run Functional Tests

The functional tests will require access to a z/OS system.
This requires minimal additional configuration.

### Configuration and Arguments

#### YAML Arguments

Create a YAML file containing information needed to run the functional tests.


| Argument    | Description                                                                                                                                                                                                                                               | Required | Aliases |
| :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------ |
| host        | The z/OS target host to connect to.                                                                                                                                                                                                                       | True     |         |
| user        | The username for authentication with host.                                                                                                                                                                                                                | True     |         |
| python_path | The absolute path to the python interpreter on the z/OS target host.                                                                                                                                                                                      | True     |         |
| environment | A list of key-value pairs containing all environment variables that need to be set on the z/OS target host before running Python/Ansible. It is important to add two sets of quotes when quotations are desired in the environment variable _export_ statement. | False    |         |

Example:

```yaml
host: tivlp02.svl.ibm.com
user: bbecker
python_path: /var/python27/python27/bin/python
environment:
    INSTALL_PYTHON: /var/python27
    RELEASE_NAME: python-2017-04-12
    RELEASE_TYPE: py27
    RELEASE_DIR: /var/python27
    PKGS_BASE: /var/python27/pkgs
    PYTHON_ENV: python27
    PYTHON_HOME: /var/python27/python27
    PYTHON: /var/python27/python27/bin
    LIBPATH: /var/python27/python27/lib:${LIBPATH}
    FFI_LIB: /var/python27/python27/lib/ffi
    TERMINFO: /var/python27/python27/share/terminfo
    PKG_CONFIG_PATH: /var/python27/python27/share/pkgconfig:/var/python27/python27/lib/pkgconfig
    CURL_CA_BUNDLE: /var/python27/python27/etc/ssl/cacert.pem
    # environment variables for mvsutils/mvscmd
    _: /hsstools/bin/env
    _BPXK_AUTOCVT: ON
    # * ensure quotations are provided correctly where needed!!
    _CEE_RUNOPTS: '"FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)"'
    _TAG_REDIR_ERR: txt
    _TAG_REDIR_IN: txt
    _TAG_REDIR_OUT: txt
    TOOLS_ROOT: /hsstools
    GIT_SHELL: /hsstools/bin/bash
    GIT_EXEC_PATH: /hsstools/git-2.14.4/libexec/git-core
    GIT_TEMPLATE_DIR: /hsstools/git-2.14.4/share/git-core/templates
    PATH: /hsstools/git-2.14.4/bin:/bin:/var/bin:/usr/lpp/java/J8.0/bin:/var/python27/python-2017-04-12-py27/python27/bin
    # Java environment
    JAVA_HOME: /usr/lpp/java/J8.0_64
```

#### CLI Arguments

__`--zinventory`__ (or __`-Z`__ ) is used to provide the absolute path to the configuration YAML file.

By default, `--zinventory` (or `-Z` ) is set to `test_config.yml` in the working directory.

Additionally, certain select arguments from [pytest-ansible](https://github.com/ansible/pytest-ansible) can be used.
These can be passed in on the command line or provided in the YAML configuration file.

Some arguments marked _NOT SUPPORTED_ may work with additional testing.

```bash
py.test \
    NOT SUPPORTED [--inventory <path_to_inventory>] \
    REQUIRED [--host-pattern <host-pattern>] \
    [--connection <plugin>] \
    BROKEN [--module-path <path_to_modules] \
    [--user <username>] \
    [--become] \
    [--become-user <username>] \
    [--become-method <method>] \
    NOT SUPPORTED [--limit <limit>] \
    [--check]
```

__`--host-pattern=all` is required to be provided.__

Normally, `module_path` in YAML config, or `--module-path` on CLI would be valid parameters, which would function as an alternative to [setting the ANSIBLE_LIBRARY environment variable](#add-module-directory-to-ansiblelibrary).
Unfortunately, the option seems to be broken in the latest Ansible release.

#### Add module directory to ANSIBLE_LIBRARY

If modules are in

```
/
└── Users
    └── myuser
        └── ansible_collections_ibm_zos_core
            └── plugins
                └── modules
```

The command to add the directory is

```bash
export ANSIBLE_LIBRARY=/Users/myuser/ansible_collections_ibm_zos_core/plugins/modules
```


__Navigate to the functional tests folder__

```
ansible_collections_ibm_zos_core
└── tests
    └── functional
```

__If Python 2 is default__

Assuming the absolute path of the YAML configuration file is `/home/myuser/test_config.yml`

```bash
python3 -m pytest --host-pattern=all --zinventory=/home/myuser/test_config.yml
```

__If Python 3 is default__

Assuming the absolute path of the YAML configuration file is `/home/myuser/test_config.yml`

```bash
pytest --host-pattern=all --zinventory=/home/myuser/test_config.yml
```

## Running Test Cases Using Bash Script

To run test cases using the bash script, enter the following commands:  
```
cd ibm_zos_ims/tests
```  
```
chmod +x run.sh
```  
```
./run.sh test_config.yml path/to/test/suite
```  
