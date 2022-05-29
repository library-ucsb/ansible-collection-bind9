# BIND9 Role

Manages the deployment of BIND9 to the following platforms:
 - Debian
 - Ubuntu

## Useful Tags
 When running the playbook, there are various tags to utilize.  Each are listed below.  Note that if one or more tags are not specified, then the complete playbook will execute.  Same as the tasks used when specifying the `role:bind9:installation` tag.

### role:bind9:rndc_key
Runs the tasks specific to the rndc keys
    
### role:bind9:installation
Runs the tasks that affect the installation of bind9.  This includes **all** of the tasks in the main playbook **site.yml**

### role:bind9:configuration
Runs the tasks that affect:
 - named.conf
 - named.conf.options
 - named.conf.local
 - /etc/defaults/bind9.conf
 - rndc keys
 - dynamic zones
 - static zones

### role:bind9:zones:change
Runs the tasks that affect:
 - dynamic zones
 - static zones

### role:bind9:backup
Runes tasks that backs up:
  - /etc/default/bind
  - /etc/logrotate.d/bind
  - /etc/bind

## Adding to Playbook

In order to use this role, you must include this collection in your playbook.

To install from git via ssh, run from within your playbook:
`
$ ansible-galaxy collection install git@github.com:library-ucsb/ansible-collection-bind9.git
`

If you need to use https, authentication is required.  Ideally the operator would generate a GitHub Personal Access Token, with the correct permissions, and insert it in the url below.  In this case replcae $(GH_TOKEN) with the token you have generated.
`
$ ansible-galaxy collection install git+https://$(GH_TOKEN)@github.com/library-ucsb/ansible-collection-bind9.git
`

If you are using one of Josh's base playbook structures, there should be a bash initialization script.  Older versions could be found in the root directory, named `initialize.sh`.  Latter playbooks have the same script in the `init/` subdirectory.  Either will essentially run the `ansible-galaxy` commands above, but read the list of collections and roles from `requirements.yml`.

Add the following entry under the `collections:` section:
```
collections:
  - name: https://github.com/library-ucsb/ansible-collection-bind9.git

```

An example of a complete `requirements.yml` file:
```
---

collections:
  - name: community.general
  - name: https://github.com/library-ucsb/ansible-collection-bind9.git
  - name: https://github.com/library-ucsb/library-ansible-collections-core.git
  - name: https://github.com/library-ucsb/library-ansible-collections-certs.git

roles:
  - name: willshersystems.sshd
  - name: singleplatform-eng.users
  - name: geerlingguy.firewall
  - name: geerlingguy.ntp
  - name: geerlingguy.docker
  - name: geerlingguy.pip
  - name: ahuffman.sudoers
  - name: sbaerlocher.snmp
```

## Essential Variables

This is a large topic that I'll split up by operator/operation.

### Ops Member / Operating System Maintenance
These variables manage the following host services:
 - unix users and groups
 - sshd
 - sudoers
 - snmpd
 - iptables
 - ntp
 - docker

 Changes for these services are almost always applied against all the `bind_servers`, so the corresponding yaml configuration documents are found under `group_vars/all/`
 Configuring these role variables is outside of the scope of this README, as there shouldn't be much to change from the defaults.

### Ops Member / BIND Maintenance

#### group_vars/all/bind9-acls.yml

```
bind9_acls:
  - name: name_of_acl
    comment: "something meaningful"
    targets:
      - "another_acl"
      - "10.99.0.1"
```

Note that the following two acls need to remain, as the underlying playbook depends on them:
```
  - name: our_neighbors
    comment: "package built-in"
    targets: "{{ bind9_our_neighbors }}"

  - name: our_networks
    comment: "package built-in"
    targets: "{{ bind9_our_networks }}"
```

#### group_vars/all/bind9-logging.yml
Affects the bind9 logging system.  Is somewhat limited presently.  You can add more categories, but I have yet to add support for creating channels.  There is only the one: `bind_log`.  It delivers to a single logfile `bind.log`, found in the path specified in `bind9_log_path`.  Note that if you change this path to a location outside of `/var/log/named`, you will also need to investigate modifying ubuntu's **apparmor** to permit writes by **bind** to a different path.

#### group_vars/all/bind9-masters.yml
Much like an `acl`, bind9 `masters` specify a grouping of hosts, but are consider **master**'s as far as a dns system is concerned.  Certain bind directives require the use of masters instead of an acl.

The general structure of the data set:
```
bind9_masters:
  - name: master_server_internal
    addresses:
      - "1.2.3.4"
      - "5.6.7.8"
```

#### group_vars/all/bind9-rndc.yml AND group_vars/all/bind9-rndc-vault.yml
Manages the **rndc** keys across the managed bind9 servers.  The sensitive key is located in the `bind9-rndc-vault.yml` file, which is encrypted with `ansible-vault`.  Within this document are the following entries:

```
vault_bind9_rndc_algo: HMAC
vault_bind9_rndc_key: 23902849829sfil292452945
```

Those two values are then referenced in the un-encrypted `bind9-rndc.yml` file.

## Ops Member / Zone Maintenance

See [docs/ZONES.md](docs/ZONES.md)

## Ops Member / GitHub Actions

See [docs/GHA.md](docs/GHA.md)