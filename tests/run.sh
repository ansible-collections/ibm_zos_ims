#!/bin/bash

current_dir=$(pwd)
# current_dir=tests
project_root=${current_dir}/../
plugins_dir=${current_dir}/../plugins
core_dir=~/.ansible/collections/ansible_collections/ibm/ibm_zos_core/plugins
export ANSIBLE_LIBRARY=${plugins_dir}/modules/:${core_dir}/modules
export ANSIBLE_MODULE_UTILS=${plugins_dir}/module_utils/:${core_dir}/module_utils
export ANSIBLE_ACTION_PLUGINS=${plugins_dir}/action
export ANSIBLE_CONNECTION_PLUGINS=${plugins_dir}/connection
export ANSIBLE_COLLECTIONS_PATH=/home/jenkins/.ansible/collections/ansible_collections
export ANSIBLE_CONFIG=${current_dir}/ansible.cfg

cd ${project_root}

python3 -m pytest -rA --host-pattern=all --zinventory=tests/test_config.yml $2 -vvv