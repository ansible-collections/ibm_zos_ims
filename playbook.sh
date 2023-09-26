# Removes the loacl tar ball, builds local version and installs the local tar ball
#rm -rf ibm-ibm_zos_ims-*.tar.gz; ansible-galaxy collection build; ansible-galaxy collection install -f ibm-ibm_zos_ims-*

# # Installs directory from galaxy
# ansible-galaxy collection install -fc ibm.ibm_zos_core:1.5.0

# Builds IMS Collection locally
ansible-galaxy collection build ./ --force
# Installs IMS local tar ball
ansible-galaxy collection install ibm-*.tar.gz -c --force-with-deps

# Installs directory from galaxy
ansible-galaxy collection install -fc ibm.ibm_zos_core:1.5.0

# Installs loacl tar ball
#ansible-galaxy collection install -f ibm-ibm_zos_core-*

current_dir=$(pwd)
plugins_dir=${current_dir}/plugins
export ANSIBLE_LIBRARY=${plugins_dir}/modules/
export ANSIBLE_MODULE_UTILS=${plugins_dir}/module_utils
export ANSIBLE_ACTION_PLUGINS=${plugins_dir}/action
export ANSIBLE_CONNECTION_PLUGINS=${plugins_dir}/connection
export ANSIBLE_CONFIG=${current_dir}/playbooks/ansible.cfg
ansible-playbook -i "$1" "$2" -vvv