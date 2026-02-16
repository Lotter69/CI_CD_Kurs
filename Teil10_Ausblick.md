## Ausblick
![line](images/banner.png)


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

9. **Sicherheit ergänzen**
   - SSH Pubkey Authentifizierung
   - Ansible Vault (Verschlüsselung sensibler Daten)

10. **Skalierbarkeit**
   - Variablen und Facts in Playbook einsetzen
        - Gruppenvariablen
        - Hostspezifische Variablen
   - Wartbarkeit komplexer Konfigurationen sicherstellen mit Vorlagen (Jinja2-Templates) sicherstellen
   - Code-Organisation bei großen Projekten mit Rollen strukturieren (Rollen für Aufgabe: z. B. Rolle für ACL-management, Rolle für Backups, Rolle für NTP-Konfiguration)
---

## Autoren und Urheberrecht
- Michael Lotter
- Date: 01/2026
- Version: v2.0

![line](images/banner.png)
<p align="center">
<a href="Teil09_ACL_Netzwerkkonfiguration_veraendern.md"><img src="images/previous.png" width="150px"></a>
</p>