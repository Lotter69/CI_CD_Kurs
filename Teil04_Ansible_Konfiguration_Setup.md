
## Teil 4: Ansible-Konfiguration Setup

### Schritt 12: Ansible-Verzeichnis erstellen

```bash
cd ~/cml-as-code-ansible
mkdir ansible
cd ansible
```

### Schritt 13: Test-Network Inventar erstellen

```bash
nano test-network.yaml
```

**Inhalt:**
```yaml
routers:
  hosts:
    router1:
      ansible_host: xxx.xxx.xxx.xxx  # ANPASSEN!
    router2:
      ansible_host: xxx.xxx.xxx.xxx  # ANPASSEN!
  vars:
    ansible_network_os: ios
    ansible_user: YoursshUser
    ansible_password: YoursshPW
    ansible_connection: network_cli
    ansible_become: yes
    ansible_become_method: enable
    ansible_become_password: Yourenapw
```

### Schritt 14: Produktiv-Network Inventar erstellen

```bash
nano production-network.yaml
```

**Inhalt:**
```yaml
routers:
  hosts:
    router1:
      ansible_host: xxx.xxx.xxx.xxx  # ANPASSEN!
    router2:
      ansible_host: xxx.xxx.xxx.xxx  # ANPASSEN!
  vars:
    ansible_network_os: ios
    ansible_user: YoursshUser
    ansible_password: YoursshPW
    ansible_connection: network_cli
    ansible_become: yes
    ansible_become_method: enable
    ansible_become_password: Yourenapw
```

### Schritt 15: Ansible Playbook erstellen

```bash
nano deploy-acl-config.yaml
```

**Inhalt:**
```yaml
---
- name: Configure ACL on Cisco routers
  hosts: routers
  gather_facts: no

  tasks:
    - name: Include ACL vars
      include_vars: '../acl-config.yaml'

    - name: Remove old ACL from interface (if exists)
      cisco.ios.ios_config:
        lines:
          - no ip access-group {{ acl[0].acls[0].name }} in
        parents: interface {{ acl_interface[0].name }}
      ignore_errors: yes

    - name: Remove old ACL (if exists)
      cisco.ios.ios_config:
        lines:
          - no ip access-list extended {{ acl[0].acls[0].name }}
      ignore_errors: yes

    - name: Build ACL rules from config
      set_fact:
        acl_rules: "{{ acl_rules | default([]) + [item.sequence | string + ' ' + item.grant + ' ' + item.protocol + ' ' + item.source.address + ' ' + item.destination.address + ((' eq ' + item.destination.port_protocol.eq) if item.destination.port_protocol is defined else '')] }}"
      loop: "{{ acl[0].acls[0].aces }}"
      loop_control:
        label: "{{ item.sequence }}"

    - name: Create ACL
      cisco.ios.ios_config:
        lines: "{{ acl_rules }}" 
        parents: ip access-list extended {{ acl[0].acls[0].name }}
        save_when: modified

    - name: Apply ACL to interface
      cisco.ios.ios_config:
        lines:
          - ip access-group {{ acl[0].acls[0].name }} {{ acl_interface[0].access_groups[0].acls[0].direction }}
        parents: interface {{ acl_interface[0].name }}
        save_when: modified
```

**Hinweise zur Konfiguration**
- Dynamisches Lesen aus `acl-config.yaml` mit `set_fact`
- Unterstützt beliebige ACL-Regeln ohne Code-Änderungen
- Verwendet `ios_config` statt `ios_acls` (IOL-Router Kompatibilität)

---

### Technischer Hintergrund: Warum ios_config statt ios_acls?

**Wichtig für das Verständnis der Architekturentscheidung:**

Dieses Lab verwendet **IOL-XE Router** (`node_definition: iol-xe`) in CML. Diese Router haben besondere Anforderungen:

#### **Strukturierte Module (ios_acls/ios_acl_interfaces) - nicht empfohlen für IOL:**

```yaml
# Funktioniert NUR zuverlässig mit echten IOS-XE Geräten (CSR1000v)
- name: Create ACL 
  cisco.ios.ios_acls:
    config: "{{ acl }}"
    state: overridden
```

**Probleme bei IOL-Routern:**
- Prompt-Handling Fehler (`Router(config)#` statt `Router#`)
- Session bleibt im Config-Modus stecken
- Inkompatibilität mit Ansible 2.13.13
- Komplexe YAML → IOS Übersetzung fehlerhaft

**Typische Fehlermeldung:**
```
The error was: Router2(config)#
fatal: [router2]: FAILED! => {"msg": "Unexpected failure during module execution."}
```

#### **Direktes ios_config Modul - empfohlen für IOL:**

```yaml
# Funktioniert zuverlässig mit IOL-Routern
- name: Create ACL
  cisco.ios.ios_config:
    lines: "{{ acl_rules }}"
    parents: ip access-list extended 110
```

**Vorteile:**
- Direkte IOS-Befehle ohne Übersetzung
- Bewährtes Modul seit Jahren stabil
- Einfacher State-Machine (Config → Befehle → Exit)
- Kompatibel mit Ansible 2.13.13
- Besseres Debugging

**Entscheidungsmatrix:**

| Router-Typ | Empfohlenes Modul | Grund |
|------------|-------------------|-------|
| **IOL-XE** (dieses Lab) | `ios_config` | ✅ Stabile Kompatibilität |
| **CSR1000v** | `ios_acls` | ✅ Strukturierte Daten möglich |
| **Physische Catalyst 9000** | `ios_acls` | ✅ Optimiert für IOS-XE |

> **Für Produktivumgebungen:** Wenn Sie später auf CSR1000v oder physische Hardware umsteigen, können Sie zu strukturierten Modulen wechseln. Für dieses Lab mit IOL-Routern ist `ios_config` die zuverlässigste Wahl!

---

### Schritt 16: Ansible-Konfigurationsdatei erstellen

```bash
cd ~/cml-as-code-ansible
nano ansible.cfg
```

**Inhalt:**
```ini
[defaults]
host_key_checking = False
deprecation_warnings = False
```

---

