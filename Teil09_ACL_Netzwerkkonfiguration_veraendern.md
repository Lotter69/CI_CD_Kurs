## Teil 9: ACL verändern (erweitern)

Jetzt fügen wir eine neue Regel hinzu, um den Workflow zu testen.

### Schritt 34: Lokales Repo aktualisieren

```bash
cd ~/cml-as-code-ansible
git checkout test
git pull origin test
```

### Schritt 35: Telnet-Regel hinzufügen

```bash
nano acl-config.yaml
```

**Telnet-Regel aktivieren (Kommentare entfernen):**

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

          # NEUE REGEL - Kommentare entfernen!
          - grant: deny 
            sequence: 30 
            protocol: tcp 
            source: 
              address: any 
            destination: 
              address: any 
              port_protocol: 
                eq: telnet
                 
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

**Speichern**

> Das Playbook liest diese Änderung automatisch und deployed sie! Kein Code muss geändert werden!

---

## Meilenstein 5: Änderung testen

```bash
git add acl-config.yaml

git commit -m "Add Telnet deny rule to ACL

- Blocks Telnet traffic (port 23)
- Sequence 30 between HTTP and permit all
- Demonstrates enhanced CI/CD workflow
- Will be tested automatically
- Dynamic configuration from YAML (no code changes!)"

git push origin test
```

**Der Workflow:**
```
git push origin test
  ↓
GitHub Actions triggert Test-Workflow
  ↓
1. Test-Netzwerk wird in CML erstellt
2. Neue ACL-Konfiguration wird deployed (automatisch aus YAML gelesen!)
3. pyATS Tests validieren Konnektivität
4. Test-Netzwerk wird gelöscht
  ↓
Tests erfolgreich? 
  ↓
Sie erstellen Pull Request
  ↓
Review & Merge to main
  ↓
Production Deployment startet automatisch
  ↓
ACL ist in Produktiv-Netz deployed!
```

Nach erfolgreichem Test:
1. Pull Request erstellen
2. Mergen
3. Automatisches Deployment für Produktiv-Netz

### Schritt 36: Produktiv-Netz verifizieren

```bash
ssh YoursshUsername@xxx.xxx.xxx.xxx
enable
show ip access-lists 110
```

**Erwartete Ausgabe:**
```
Extended IP access list 110
    20 deny tcp any any eq www
    30 deny tcp any any eq telnet  # NEU!
    40 permit ip any any
```

---

### Die CI/CD-Pipeline im Detail

**Test-Phase (Branch: test):**
```yaml
1. Starte das Test-Netzwerk in CML
   - Dynamische Erstellung virtueller Router
   - Isolierte Test-Umgebung
   
2. Überprüfe die ACL-Konfiguration
   - Deploy mit Ansible (dynamisch aus YAML)
   - SSH Cleanup
   - Automatisierte Tests mit pyATS
   
3. Lösche das Test-Netzwerk in CML
   - Cleanup nach Tests
   - Ressourcen freigeben
   - Verbessertes Error-Handling
```

**Produktiv-Phase (Branch: main):**
```yaml
4. Bereitstellung für reales Netz
   - Deployment auf persistente Router
   - Verifizierung
   - Dokumentation
```
---

## Ausblick: Nächste Schritte

Nach diesem Lab können Sie:

1. **Weitere ACL-Regeln hinzufügen**
   - FTP, SMTP, HTTPS, etc.
   - Spezifische IP-Ranges
   - Einfach durch Bearbeiten von acl-config.yaml!

2. **Alternative CML-Lab-Verwaltung**
   - REST-API statt PyPi

3. **Mehr Tests implementieren**
   - ACL-Verifizierung
   - Compliance-Checks
   - Performance-Tests

4. **Alternative Netzwerk-Automatisierungs-Werkzeuge**
   - Network Service Orchestrator (NSO) statt Ansible
   - Terraform statt Ansible

5. **Alternative DVCS**
   - GitLab statt GitHub

6. **Alternative Virtualisierungs-Umgebungen**
   - GNS3 statt CML
   - EVE NG statt CML

7. **Auf echte Hardware übertragen**
   - Produktiv-Inventar auf echte IPs anpassen
   - Bei CSR1000v: Wechsel zu ios_acls Modulen möglich
   - Gleicher Workflow funktioniert

8. **Pipeline erweitern**
   - Notifications (Slack, Email)
   - Rollback-Mechanismen
   - Staging-Umgebung

---

## Autoren und Urheberrecht
- Michael Lotter
- Date: 01/2026
- Version: v2.0

![line](../images/banner.png)
<p align="center">
<a href="../01-why-automation/1.md"><img src="../../images/previous.png" width="150px"></a>
<a href="../02-intro-to-apis/1.md"><img src="../../images/next.png" width="150px"></a>
</p>