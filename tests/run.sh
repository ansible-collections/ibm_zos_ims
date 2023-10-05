#!/bin/bash

ansible-galaxy collection build ../ --force
ansible-galaxy collection install ./ibm-ibm_zos_ims*.tar.gz -c -f --force-with-deps

# Installs directory from galaxy
ansible-galaxy collection install -fc ibm.ibm_zos_core:1.5.0

current_dir=$(pwd)
plugins_dir=${current_dir}/../plugins
core_dir=~/.ansible/collections/ansible_collections/ibm/ibm_zos_core/plugins
export ANSIBLE_LIBRARY=${plugins_dir}/modules/:${core_dir}/modules
export ANSIBLE_MODULE_UTILS=${plugins_dir}/module_utils${core_dir}/module_utils
export ANSIBLE_ACTION_PLUGINS=${plugins_dir}/action
export ANSIBLE_CONNECTION_PLUGINS=${plugins_dir}/connection
export ANSIBLE_CONFIG=${current_dir}/ansible.cfg

python3 -m pytest --host-pattern=all --zinventory="${1:-test_config.yml}" "$2" -vvv

# python3 -m pytest --zinventory="${1:-test_config.yml}" "$2" -vvv

# ./run.sh test_config.yml functional/modules/ims_data_definition_utility/test_ims_data_definition_valid_input.py