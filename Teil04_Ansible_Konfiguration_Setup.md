
## Teil 4: Ansible-Konfiguration Setup
![line](images/banner.png)
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
----
# Ansible Playbook: ACL-Konfiguration auf Cisco-Router deployen
# Wird aufgerufen mit:
#   ansible-playbook -i ansible/test-network.yaml ansible/deploy-acl-config.yaml
#   ansible-playbook -i ansible/production-network.yaml ansible/deploy-acl-config.yaml

- name: Configure ACL on Cisco routers
  hosts: routers        # Zielgruppe aus dem Inventar (test-network.yaml / production-network.yaml)
  gather_facts: no      # Keine automatische Inventarisierung des Routers – spart Zeit

  tasks:

    # -------------------------------------------------------------------------
    # SCHRITT 1: Konfiguration einlesen
    # -------------------------------------------------------------------------
    - name: Include ACL vars
      # Liest acl-config.yaml ein und stellt alle darin definierten Variablen
      # (acl, acl_interface) für die nachfolgenden Tasks zur Verfügung.
      include_vars: '../acl-config.yaml'


    # -------------------------------------------------------------------------
    # SCHRITT 2: Alte ACL vom Interface entfernen
    # -------------------------------------------------------------------------
    - name: Remove old ACL from interface (if exists)
      cisco.ios.ios_config:
        lines:
          # IOS-Befehl: Entfernt die ACL-Zuweisung vom Interface.
          # {{ acl[0].acls[0].name }} → ACL-Name aus acl-config.yaml, z.B. "110"
          - no ip access-group {{ acl[0].acls[0].name }} in
        # parents: bestimmt den Konfigurationskontext, d.h. den übergeordneten
        # IOS-Befehl, unter dem die lines ausgeführt werden.
        # {{ acl_interface[0].name }} → Interface-Name aus acl-config.yaml, z.B. "Ethernet0/1"
        parents: interface {{ acl_interface[0].name }}
      # ignore_errors: Falls die ACL noch nicht existiert, wird der Fehler
      # ignoriert und das Playbook läuft weiter – idempotentes Verhalten.
      ignore_errors: yes


    # -------------------------------------------------------------------------
    # SCHRITT 3: Alte ACL-Definition löschen
    # -------------------------------------------------------------------------
    - name: Remove old ACL (if exists)
      cisco.ios.ios_config:
        lines:
          # IOS-Befehl: Löscht die gesamte ACL-Definition.
          # Notwendig, damit veraltete Regeln nicht erhalten bleiben.
          - no ip access-list extended {{ acl[0].acls[0].name }}
      ignore_errors: yes  # Gleiche Logik wie oben: ACL muss nicht existieren


    # -------------------------------------------------------------------------
    # SCHRITT 4: ACL-Regeln aus acl-config.yaml zusammenbauen
    # -------------------------------------------------------------------------
    - name: Build ACL rules from config
      # set_fact erstellt zur Laufzeit eine neue Variable (acl_rules).
      # Sie enthält am Ende eine Liste von IOS-Befehlen, z.B.:
      #   ["20 deny tcp any any eq www", "40 permit ip any any"]
      set_fact:
        # acl_rules wird schrittweise aufgebaut: Bei jedem Loop-Durchlauf wird
        # ein neuer Eintrag an die bestehende Liste angehängt.
        # default([]) stellt sicher, dass die Variable beim ersten Durchlauf
        # als leere Liste startet.
        acl_rules: "{{ acl_rules | default([]) + [item.sequence | string + ' ' + item.grant + ' ' + item.protocol + ' ' + item.source.address + ' ' + item.destination.address + ((' eq ' + item.destination.port_protocol.eq) if item.destination.port_protocol is defined else '')] }}"
        # Aufbau eines Regeleintrags Schritt für Schritt:
        #   item.sequence          → Sequenznummer,      z.B. "20"
        #   item.grant             → Aktion,             z.B. "deny" oder "permit"
        #   item.protocol          → Protokoll,          z.B. "tcp" oder "ip"
        #   item.source.address    → Quell-Adresse,      z.B. "any"
        #   item.destination.address → Ziel-Adresse,     z.B. "any"
        #   item.destination.port_protocol.eq (optional) → Port, z.B. "www" oder "telnet"
        #     → wird nur ergänzt, wenn port_protocol in der Regel definiert ist

      # loop iteriert über alle Einträge unter aces: in acl-config.yaml.
      # Jede Regel (deny www, permit ip, ...) wird einmal durchlaufen.
      loop: "{{ acl[0].acls[0].aces }}"

      loop_control:
        # label sorgt dafür, dass in der Ansible-Ausgabe nur die Sequenznummer
        # angezeigt wird (statt des gesamten loop-Objekts) – bessere Lesbarkeit.
        label: "{{ item.sequence }}"


    # -------------------------------------------------------------------------
    # SCHRITT 5: ACL auf dem Router anlegen
    # -------------------------------------------------------------------------
    - name: Create ACL
      cisco.ios.ios_config:
        # lines enthält die in Schritt 4 gebaute Regelliste.
        # Ansible übergibt sie als einzelne IOS-Befehle an den Router.
        lines: "{{ acl_rules }}"
        # parents setzt den Konfigurationskontext:
        # Alle lines werden unterhalb von "ip access-list extended 110" ausgeführt.
        parents: ip access-list extended {{ acl[0].acls[0].name }}
        # save_when: modified → Router speichert die Konfiguration nur,
        # wenn tatsächlich eine Änderung vorgenommen wurde (effizient & sicher).
        save_when: modified


    # -------------------------------------------------------------------------
    # SCHRITT 6: ACL dem Interface zuweisen
    # -------------------------------------------------------------------------
    - name: Apply ACL to interface
      cisco.ios.ios_config:
        lines:
          # IOS-Befehl: Weist die ACL dem Interface in der definierten Richtung zu.
          # acl[0].acls[0].name    → ACL-Name,    z.B. "110"
          # acl_interface[0].access_groups[0].acls[0].direction → Richtung, z.B. "in"
          - ip access-group {{ acl[0].acls[0].name }} {{ acl_interface[0].access_groups[0].acls[0].direction }}
        # Interface-Kontext, z.B. "interface Ethernet0/1"
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

![line](images/banner.png)
<p align="center">
<a href="Teil03_CML-Test-Netzwerk-Setup.md"><img src="images/previous.png" width="150px"></a>
<a href="Teil05_Netzwerk-Konfiguration.md"><img src="images/next.png" width="150px"></a>
</p>