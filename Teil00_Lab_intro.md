# Lab - Erstellen einer CI/CD-Pipeline zum Testen der Ansible-Konfiguration in einem CML-Netzwerk
![line](images/banner.png)

**Angepasst für: Linux Mint + GitHub + CML Personal 2.9**

## Überblick

### Berufliche Aufgabenstellung

Sie sind Fachinformatiker in einem Unternehmen und verantwortlich für die Verwaltung der Netzwerk-Sicherheitskonfigurationen. Ihre Aufgabe ist es, Access Control Lists (ACLs) auf Routern zu konfigurieren und zu pflegen. 

**Herausforderung:** Manuelle Konfigurationsänderungen sind fehleranfällig und zeitaufwändig. Jede Änderung muss getestet werden, bevor sie im Produktiv-Netzwerk ausgerollt wird. Die bisherige Methode – manuelle Tests in einem separaten Testaufbau – ist ineffizient und führt zu langen Änderungszyklen.

**Lösung:** Sie implementieren eine automatisierte CI/CD-Pipeline (Continuous Integration/Continuous Deployment), die:
1. **Konfigurationen als Code verwaltet** (Infrastructure as Code mit Ansible)
2. **Änderungen automatisch testet** in einem virtualisierten Testnetzwerk
3. **Validierte Konfigurationen automatisch ausrollt** ins Produktiv-Netzwerk

### Anforderungen an die Pipeline

Die Pipeline durchläuft bei jeder Änderung folgende Phasen:

```
Entwickler/Engineer macht ACL-Änderung
  ↓
Commit & Push zu GitHub (Branch: test)
  ↓
╔═══════════════════════════════════════════════════════╗
║  AUTOMATISCHE TEST-PHASE (in GitHub Actions)          ║
╠═══════════════════════════════════════════════════════╣
║  1. Start Test-Netzwerk in CML                        ║
║     → 2 virtuelle Cisco Router werden gestartet       ║
║                                                       ║
║  2. Deploy ACL-Konfiguration auf Test-Router          ║
║     → Ansible wendet neue ACL an                      ║
║                                                       ║
║  3. Automatische Tests (pyATS)                        ║
║     → Konnektivitätstests                             ║
║     → Funktionsprüfung                                ║
║                                                       ║
║  4. Cleanup: Test-Netzwerk wird gelöscht              ║
╚═══════════════════════════════════════════════════════╝
  ↓
Tests erfolgreich? 
  ↓
Pull Request: test → main
  ↓
Review & Merge
  ↓
╔═══════════════════════════════════════════════════════╗
║  AUTOMATISCHE DEPLOYMENT-PHASE DER PRODUKIV-UMGEBUNG  ║
╠═══════════════════════════════════════════════════════╣
║  1. Ansible deployed ACL auf Produktiv-Router         ║
║     → Konfiguration wird ausgerollt                   ║
║                                                       ║
║  2. Verifizierung                                     ║
║     → Deployment-Status wird geprüft                  ║
╚═══════════════════════════════════════════════════════╝
  ↓
Produktiv-Umgebung ist aktualisiert! 
```

### Labor-Umgebung

**In diesem Lab simulieren wir ein realistisches Szenario:**

| Umgebung | Beschreibung | Technologie | Automatisierung |
|----------|--------------|-------------|-----------------|
| **Test-Netzwerk** | Automatisch erstelltes virtuelles Netzwerk für Tests | CML (2 virtuelle Router - nur temporär vorhanden) | Wird bei jedem Test-Lauf neu erstellt & gelöscht |
| **Produduktiv-Netzwerk** | Simuliertes "Produktiv-Netzwerk" für das Labor | CML (2 virtuelle Router - dauerhaft vorhanden) | Konfiguration wird automatisch deployed |

**Wichtig zu verstehen:**
- **Test-Netzwerk:** Wird **dynamisch** in CML erstellt (on-demand), getestet und wieder gelöscht
- **Produktiv-Netzwerk:** Läuft **permanent** in CML und simuliert Ihr "echtes" Netzwerk
- **In der Realität** würde das Produktiv-Netzwerk auf echter Hardware laufen
- **In diesem Lab** nutzen wir CML für beide Umgebungen, um die Infrastruktur zu simulieren

**Warum diese Aufteilung?**
```
Test-Netzwerk (temporär):
  ├─ Isolierte Umgebung für Experimente
  ├─ Kann ohne Risiko zerstört werden
  ├─ Automatisch erstellt/gelöscht
  └─ Validiert Änderungen vor Production

Production-Netzwerk (dauerhaft):
  ├─ Simuliert Ihr "echtes" Unternehmensnetzwerk
  ├─ Änderungen nur nach erfolgreichen Tests
  ├─ Läuft kontinuierlich
  └─ Erhält nur geprüfte Konfigurationen
```

### Technologie-Stack

**Was Sie in diesem Lab lernen und nutzen:**

| Komponente | Zweck | Technologie |
|------------|-------|-------------|
| **Infrastructure as Code** | Netzwerkkonfiguration als versionierte Dateien | Ansible + YAML |
| **Virtualisierung** | Netzwerk-Simulation | Cisco Modeling Labs (CML) 2.9 |
| **Versionskontrolle** | Code-Management und Kollaboration | Git + GitHub |
| **CI/CD-Plattform** | Automatisierung der Pipeline | GitHub Actions |
| **Test-Automation** | Automatische Netzwerk-Tests | pyATS/Genie |
| **Deployment-Automation** | Automatisches Konfigurationsmanagement | Ansible |

### Nutzen für die Praxis

Nach Abschluss dieses Labs können Sie:

1. **Schnellere Änderungszyklen**
   - Statt Stunden/Tage nur noch Minuten bis zur Production-Deployment
   - Automatische Tests eliminieren manuelle Testphasen

2. **Höhere Qualität**
   - Jede Änderung wird automatisch getestet
   - Fehler werden erkannt, bevor sie das Produktiv-Netz erreichen
   - Konsistente Konfigurationen durch Code

3. **Bessere Nachvollziehbarkeit**
   - Alle Änderungen sind in Git dokumentiert
   - Wer hat wann was geändert? → Git History
   - Einfaches Rollback bei Problemen

4. **Skalierbarkeit**
   - Gleicher Prozess für 2 oder 200 Router
   - Parallele Deployments möglich
   - Wiederverwendbare Workflows

### Repository-Struktur

```
~/cml-as-code-ansible/              # Git Repository
├── venv/                           # Python-Umgebung (LOKAL)
├── ansible.cfg                     # Ansible SSH-Konfiguration
├── acl-config.yaml                 # ACL-Definition (Infrastructure as Code)
├── testbed.yaml                    # pyATS Testbed-Definition
├── test.py                         # Automatisierter Konnektivitätstest
├── python/
│   ├── test-network.py            # CML Test-Netzwerk Management
│   ├── ansible-test-lab.yaml      # CML Topologie für Tests
│   └── requirements.txt           # Python-Dependencies
├── ansible/
│   ├── deploy-acl-config.yaml     # Ansible Playbook
│   ├── test-network.yaml          # Test-Router Inventar
│   └── production-network.yaml    # Production-Router Inventar
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # CI/CD-Pipeline Definition
└── .gitignore
```

### Lernziele

Nach Abschluss dieses Labs können Sie:
- Netzwerkkonfigurationen mit Ansible als Code verwalten
- Eine vollständige CI/CD-Pipeline für Netzwerk-Automation aufbauen
- CML-Umgebungen programmatisch erstellen und verwalten
- Automatisierte Tests mit pyATS/Genie implementieren
- GitHub Actions für Infrastructure-Workflows einsetzen
- Infrastructure as Code Best Practices anwenden
- Test- und Produktiv-Umgebungen professionell trennen

---

## Voraussetzungen

### Informationen die Sie benötigen

**Bevor Sie beginnen, ermitteln Sie:**

1. **CML-Server:**
   - IP-Adresse: z.B. `https://192.168.178.31`
   - Username: z.B. `IhrUsername`
   - Password: z.B. `IhrPassword`

2. **Test-Netzwerk Router IPs:**
   - Router 1: z.B. `192.168.178.201`
   - Router 2: z.B. `192.168.178.202`

3. **Produktiv-Netzwerk Router IPs:**
   - Router 1: z.B. `192.168.178.203`
   - Router 2: z.B. `192.168.178.204`
   - [CML-yaml-Datei](../01-why-automation/code/Produktiv-Netz_(dauerhaft_in_Betrieb)-Vorlage.yaml), geeignet für cml4free

![line](./images/prod_net_permanent.png)

> **Wichtiger Hinweis:** Zur Erprobung der Laborübung wurden die priv. IP-Adressen eines Heimnetzwerks verwendet: CML-Server `192.168.178.31`. Das virtualisierte Netz ist mit dem realen Netz gebridged. Beide Netze verwenden also das gleiche IP-Netz `192.168.178.0/24`. Sie müssen die IPs an Ihre Umgebung entsprechend anpassen!

---
![line](../images/banner.png)
<p align="center">
<a href="../01-why-automation/1.md"><img src="images/previous.png" width="150px"></a>
<a href="../02-intro-to-apis/1.md"><img src="images/next.png" width="150px"></a>
</p>