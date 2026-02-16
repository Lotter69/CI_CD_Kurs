
## Teil 6: pyATS Test erstellen
![line](images/banner.png)
### Schritt 18: pyATS Testbed-Datei erstellen

```bash
nano testbed.yaml
```

**Inhalt:**
```yaml
testbed:
  credentials:
    default:
      username: YoursshUsername
      password: YoursshPW
      enable:
        password: YourenaPW

devices:
  Router1:
    connections:
      cli:
        ip: xxx.xxx.xxx.xxx  
        port: 22
        protocol: ssh
        ssh_options: "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    os: iosxe
    type: iosxe

  Router2:
    connections:
      cli:
        ip: xxx.xxx.xxx.xxx
        port: 22
        protocol: ssh
        ssh_options: "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    os: iosxe
    type: iosxe
```

### Schritt 19: pyATS Test-Script erstellen

```bash
nano test.py
```

**Inhalt:**
```python
from genie.testbed import load
import sys

testbed = load('testbed.yaml')
device = testbed.devices["Router1"]
device.connect(learn_hostname = True)

test = device.execute("ping xxx.xxx.xxx.xxx")

if "!!" in test:
    print("Ping successful")
else:
    print("Ping unsuccessful")
    sys.exit(1)
```

---

## Meilenstein 1: Lokale Konfiguration testen

### Schritt 20: Manuell Test-Netzwerk in CML starten

**Auf der CML-Weboberfläche:**
1. Lab importieren: `python/ansible-test-lab.yaml`
2. Lab starten
3. Warten bis Router booted sind

### Schritt 21: Ansible Playbook lokal testen

```bash
cd ~/cml-as-code-ansible
source venv/bin/activate

ansible-playbook -i ansible/test-network.yaml ansible/deploy-acl-config.yaml
```

**Erwartete Ausgabe:**
```
PLAY [Configure ACL on Cisco routers] ******************************************

TASK [Include ACL vars] ********************************************************
ok: [router1]
ok: [router2]

TASK [Remove old ACL from interface (if exists)] *******************************
ok: [router1]
ok: [router2]

TASK [Remove old ACL (if exists)] **********************************************
ok: [router1]
ok: [router2]

TASK [Build ACL rules from config] *********************************************  # 
ok: [router1] => (item=20)
ok: [router1] => (item=40)
ok: [router2] => (item=20)
ok: [router2] => (item=40)

TASK [Create ACL] **************************************************************
changed: [router1]
changed: [router2]

TASK [Apply ACL to interface] **************************************************
changed: [router1]
changed: [router2]

PLAY RECAP *********************************************************************
router1                    : ok=6    changed=2    ...
router2                    : ok=6    changed=2    ...
```

### Schritt 22: Verbindung zu Router testen

```bash
ssh YoursshUsername@xxx.xxx.xxx.xxx
# Password: ciscoYoursshPW
```

**Auf dem Router:**
```
Router1> enable
# Password: YourenaPW

Router1# show ip access-lists 110
```

**Erwartete Ausgabe:**
```
Extended IP access list 110
    20 deny tcp any any eq www
    40 permit ip any any
```

### Schritt 23: pyATS-Test ausführen

```bash
cd ~/cml-as-code-ansible
python test.py
```

**Erwartete Ausgabe:**
```
Ping successful
```

---

## Meilenstein 2: Erste Commits

### Schritt 24: Git Status prüfen

```bash
git status
```

### Schritt 25: Dateien committen

```bash
git add .
git commit -m "Initial setup"

git push origin test
```

---

![line](images/banner.png)
<p align="center">
<a href="../01-why-automation/1.md"><img src="images/previous.png" width="150px"></a>
<a href="../02-intro-to-apis/1.md"><img src="images/next.png" width="150px"></a>
</p>