#!/bin/bash

ansible-galaxy collection build ../ --force
ansible-galaxy collection install ./ibm-ibm_zos_ims*.tar.gz --force

plugins_dir=$(pwd)/../plugins
export ANSIBLE_LIBRARY=${plugins_dir}/modules/
export ANSIBLE_MODULE_UTILS=${plugins_dir}/module_utils
export ANSIBLE_ACTION_PLUGINS=${plugins_dir}/action
export ANSIBLE_CONNECTION_PLUGINS=${plugins_dir}/connection
export ANSIBLE_CONFIG=$(pwd)/ansible.cfg

python3 -m pytest --host-pattern=all --zinventory=${1:-test_config.yml} $2
