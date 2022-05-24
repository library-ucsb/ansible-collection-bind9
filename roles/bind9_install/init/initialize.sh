#!/bin/bash

# make the 'logs' dir if not there
mkdir -p logs group_vars/all host_vars/all

# Install Ansible Galaxy Roles
printf "[*] Installing Ansible Galaxy Roles...\n"
ansible-galaxy install -r requirements.yml --force

printf "[*] Done.\n"
exit 0
