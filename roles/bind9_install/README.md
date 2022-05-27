# BIND9 Role

Manages the deployment of BIND9 to the following platforms:
 - Debian
 - Ubuntu

 When running the playbook, there are various flags to employ:

### role:bind9:rndc_key
Runs the tasks specific to the rndc keys
    
### role:bind9:installation
Runs the tasks that affect the installation of bind9.  This includes **all** of the tasks in the main playbook **sitey.yml**

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