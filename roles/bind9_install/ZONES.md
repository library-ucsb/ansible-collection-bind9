# BIND9 Zones

There are two types of zones - dynamic and static.  **Dynamic** zones are generated from yaml, where **static** zones are pre-existing zonefiles.  We exclusively leverage the **dynamic** generation of zones.  The following outlines where to find these files, and how to modify.

Also note that presently **there is no auto-increment of zone serial numbers**!  This is left to the operator to handle.


## group_vars/primaries

Here you will find variable definitions that will apply to hosts we consider to be **primaries** in the dns heiarchy.  These hosts are defined within the **inventory.yml** file.

### bind9.yml
Values you apply here will take precedent over the same defined in the `group_vars/all` directory.  Here are the more commonly modified variables at this level.

```
bind9_slaves:
  - library-slave-1
  - library-slave-2
```

```
bind_our_neighbors:
  - library-master-1
  - library-slave-2
  - campus-ns-1
```

### zones.yml
Here is where the bulk of the work is done.  In this file you will find the `zones_library_domains` variable, responsible for all of our dynamically generated zones.

Each zone entry has the following key properties:
```
    # The zone name, not meant as a friendly name.
  - name: library.ucsb.edu
    
    # true == reverse lookup zone, false == forward lookup zone
    reverse: false
    
    # master or slave
    zone_type: master
    
    # default record time-to-live in seconds
    default_ttl: 600
    
    # the zone serial number!!!!
    serial: 2022040500
    
    # default record refresh interval
    refresh: 3h
    
    # default record retry interval
    retry: 1H
    
    # default record expiry
    expire: 1000H
    
    # the zone's primary NS server's FQDN
    primary: ns1.library.ucsb.edu
    
    # the zone's contact
    admin: sysadmin.library.ucsb.edu
```

The following tend to not need modifying now that they are in place.
```
    also_notify:
      - slave_servers_internal

    allow_notify:
      - master_servers_internal
    
    allow_transfer:
      - campus_name_servers
      - slave_servers_internal

    ns_records:
      - ns1.library.ucsb.edu
      - ns2.library.ucsb.edu
      - ns1.ucsb.edu
      - ns2.ucsb.edu

    a_records:
      - 128.111.87.248

    mx_records:
      - name: aspmx.l.google.com
        priority: 1
      - name: alt1.aspmx.l.google.com
        priority: 5
      - name: alt2.aspmx.l.google.com
        priority: 5
      - name: aspmx2.googlemail.com
        priority: 10
      - name: aspmx3.googlemail.com
        priority: 10
```

Subdomain delegations are popular with our domain.  These are defined within the `subdomain_delegations` variable.

```
subdomain_delegations:
  - name: subdomain.library.ucsb.edu.
    nameservers:
      - other-name-server-001
      - other-name-server-002
```

#### RRS:
This section is where the records are maintained.  The general structure:
```
- label: the_hostname
  type: record_type      # A, TXT, PTR, CNAME, MX, SVR
  ttl: 60                # optional
  rdata: the_data        # this is the content returned by bind9 when queried for this record.
```

Example A record:
```
- label: "server-001"
  type: A
  rdata: 128.111.87.99
```

Example CNAME record:
```
- label: "server-alias"
  type: CNAME
  rdata: "server-001.library.ucsb.edu."
```

Example PTR record:
```
- label: "99"
  type: PTR
  rdata: server-001.library.ucsb.edu.
```

Example MX Record with weight:
```
- label: lists.library.ucsb.edu.
  ttl: 60
  type: MX 
  rdata: 10 lists.connect.ucsb.edu.
```

Example of a TXT record:
```
- label: lists.library.ucsb.edu.
  type: TXT 
  rdata: "v=spf1 a mx include:_spf.ucsb.edu ~all"
```