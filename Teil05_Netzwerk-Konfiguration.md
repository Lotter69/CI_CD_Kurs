## Teil 5: ACL-Konfiguration

### Schritt 17: ACL-Konfigurationsdatei erstellen

```bash
cd ~/cml-as-code-ansible
nano acl-config.yaml
```

**Inhalt:**
```yaml
---
acl:
  - afi: ipv4
    acls:
      - name: 110
        aces:
          - grant: deny
            sequence: 20
            protocol: tcp
            source:
              address: any
            destination:
              address: any
              port_protocol:
                eq: www

          # NEUE REGEL (später aktivieren)
#          - grant: deny 
#            sequence: 30 
#            protocol: tcp 
#            source: 
#              address: any 
#            destination: 
#              address: any 
#              port_protocol: 
#                eq: telnet
                 
          - grant: permit
            sequence: 40
            protocol: ip
            source:
              address: any
            destination:
              address: any                  

acl_interface:
  - name: Ethernet0/1 
    access_groups:
      - afi: ipv4
        acls:
          - name: 110
            direction: in
```



