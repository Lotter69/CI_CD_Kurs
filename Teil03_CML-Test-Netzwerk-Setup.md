
## Teil 3: CML Test-Netzwerk-Management Setup
![line](images/banner.png)
### Schritt 10: Test-Netzwerk Python-Script erstellen

```bash
nano test-network.py
```

**Inhalt:**
```python
from virl2_client import ClientLibrary
import sys

CML_SERVER = "https://xxx.xxx.xxx.xxx"  # ANPASSEN!
LAB_FILE = "ansible-test-lab.yaml"
CML_USER = "YourUser"  # ANPASSEN!
CML_PASS = "YourPW"  # ANPASSEN!
LAB_NAME = "Test-Netz"  # 

client = ClientLibrary(CML_SERVER, CML_USER, CML_PASS, ssl_verify=False)

def start_network():
    try:
        # Load the lab from a local file
        with open(LAB_FILE, "r") as lab_file:
            lab = client.import_lab(lab_file.read())

        print("Das Test-Lab wurde hergestellt!")
        print("Die Nodes werden nun gestartet...")
        # Start the lab
        lab.start()

        print("Das Test-Lab wurde gestartet")
        print("Lab ID:", lab.id)
    except Exception as e:
        print("An error occurred:", str(e))

def remove_network():
    try:
        print(f"Checking if '{LAB_NAME}' exists for removal...")
        labs = list(client.find_labs_by_title(LAB_NAME))
        
        # Warnung wenn kein Lab gefunden wurde
        if not labs:
            print(f"WARNING: No lab found with title '{LAB_NAME}'")
            return
            
        for lab in labs:
            print(f"Lab wird entfernt {lab}")
            lab.stop()
            lab.wipe()
            lab.remove()
            print("Lab wurde erfolgreich entfernt")
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py [up/down]")
        sys.exit(1)

    action = sys.argv[1]
    if action == "up":
        start_network()
    elif action == "down":
        remove_network()
    else:
        print("Invalid argument. Use 'up' to start the network or 'down' to remove it.")
        sys.exit(1)
```

**Speichern:** `Strg+O`, `Enter`, `Strg+X`

> **Wichtig:** Passen Sie `CML_SERVER`, `CML_USER` und `CML_PASS` an Ihre Umgebung an!

### Schritt 11: CML Topologie-Datei erstellen

Diese Datei finden Sie in Ihrem Vorlagen-Ordner oder erstellen sie in CML und exportieren sie.

```bash
nano ansible-test-lab.yaml
```

**Minimale Struktur** (vollständige YAML aus Vorlagen-Ordner verwenden):
```yaml
lab:
  title: Test-Netz  # Muss mit LAB_NAME übereinstimmen!
  description: Test-Netz für Validierung vor Produktivlauf
  version: 0.3.0

nodes:
  - id: n0
    label: Router1
    node_definition: iol-xe
    # ... weitere Konfiguration
    
  - id: n1
    label: Router2
    node_definition: iol-xe
    # ... weitere Konfiguration

# ... Links, Annotations, etc.
```

> **Tipp:** Die vollständige YAML-Datei finden Sie in den Vorlagen oder exportieren Sie ein vorbereitetes Lab aus CML!

---
