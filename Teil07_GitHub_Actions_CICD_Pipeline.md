
## Teil 7: GitHub Actions CI/CD Pipeline
![line](images/banner.png)
### Schritt 26: GitHub Runner installieren

**Wichtig:** Der GitHub Runner muss auf demselben System wie CML installiert sein oder Netzwerkzugriff auf CML haben!

**Auf GitHub:**
1. Settings → Actions → Runners
2. **New self-hosted runner**
3. Wählen: **Linux**
4. Folgen Sie den Anweisungen:

```bash
# Download
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.321.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.321.0/actions-runner-linux-x64-2.321.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.321.0.tar.gz

# Konfigurieren
./config.sh --url https://github.com/IhrUsername/cml-as-code-ansible --token IHR_TOKEN

# Runner starten
./run.sh
```

**In einem separaten Terminal:**
```bash
# Als Service einrichten
cd ~/actions-runner
sudo ./svc.sh install
sudo ./svc.sh start
```

**Verifizieren:**
- Auf GitHub: Settings → Actions → Runners
- Status sollte "Idle" sein 

### Schritt 27: Workflow-Verzeichnis erstellen

```bash
cd ~/cml-as-code-ansible
mkdir -p .github/workflows
cd .github/workflows
```

### Schritt 28: CI/CD Pipeline definieren

```bash
nano ci-cd.yml
```

**Inhalt:**
```yaml
name: Ansible Network CI/CD

on:
  push:
    branches:
      - test
      - main
  pull_request:
    branches:
      - main

env:
  CML_HOST: ${{ secrets.CML_HOST }}
  CML_USERNAME: ${{ secrets.CML_USERNAME }}
  CML_PASSWORD: ${{ secrets.CML_PASSWORD }}
  ANSIBLE_HOST_KEY_CHECKING: False
  ANSIBLE_PERSISTENT_CONNECT_TIMEOUT: "30"
  ANSIBLE_NETWORK_CLI_SSH_TYPE: paramiko

jobs:
  # Job 1: Build & Start Test Network (nur für test branch)
  start-test-network:
    name: Starte das Test-Netzwerk in CML
    runs-on: self-hosted
    if: github.ref == 'refs/heads/test'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python virtual environment
        run: |
          python3.8 -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r python/requirements.txt
        shell: bash
      
      - name: Starte das Test-Netzwerk
        run: |
          source venv/bin/activate
          python --version
          pip show virl2-client
          cd python
          python test-network.py up
        shell: bash
  
  # Job 2: Test Configuration
  test-configuration:
    name: Überprüfe die ACL-Konfiguration
    runs-on: self-hosted
    needs: start-test-network
    if: github.ref == 'refs/heads/test'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python virtual environment
        run: |
          python3.8 -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r python/requirements.txt
        shell: bash
      
      - name: Install Ansible collection
        run: |
          source venv/bin/activate
          ansible-galaxy collection install cisco.ios
        shell: bash
      
      - name: Test-Netzwerk bereitstellen
        run: |
          source venv/bin/activate
          ansible-playbook -i ansible/test-network.yaml ansible/deploy-acl-config.yaml
        shell: bash
      
      - name: Warte bis die Konfiguration in Betrieb genommen wurde
        run: sleep 30
        shell: bash
      
      - name: Bereinige in der know_host-Datei die ssh Einträge
        run: |
          ssh-keygen -f ~/.ssh/known_hosts -R 192.168.178.201 2>/dev/null || true
          ssh-keygen -f ~/.ssh/known_hosts -R 192.168.178.202 2>/dev/null || true
        shell: bash
      
      - name: Starte den pyATS Konnektivitäts-Test
        run: |
          source venv/bin/activate
          python test.py
        shell: bash
  
  # Job 3: Lösche das Test-Netzwerk (nur für test branch)
  cleanup-test-network:
    name: Lösche des Test-Netzwerk in CML
    runs-on: self-hosted
    needs: test-configuration
    if: always() && github.ref == 'refs/heads/test'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python virtual environment
        run: |
          python3.8 -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r python/requirements.txt
        shell: bash
      
      - name: Stoppe und entferne das Test-Netzwerk
        run: |
          source venv/bin/activate
          cd python
          python test-network.py down
        shell: bash
  
  # Job 4: Bereitstellung für die Produktivumgebung (nur für main branch)
  deploy-production:
    name: Bereitstellung für reales Netz
    runs-on: self-hosted
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python virtual environment
        run: |
          python3.8 -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r python/requirements.txt
        shell: bash
      
      - name: Install Ansible collection
        run: |
          source venv/bin/activate
          ansible-galaxy collection install cisco.ios
        shell: bash
      
      - name: Bereitstellung der ACL-Konfiguration für das reale Netz
        run: |
          source venv/bin/activate
          ansible-playbook -i ansible/production-network.yaml ansible/deploy-acl-config.yaml
        shell: bash
      
      - name: Bereitstellung überprüfen
        run: |
          echo "✓ Configuration deployed to production network"
          echo "  Router1: 192.168.178.203"
          echo "  Router2: 192.168.178.204"
        shell: bash
```

**Speichern**

> **Hinweis: Das Produktiv-Lab läuft permanent in CML und wird nicht automatisch gestartet/gestoppt!

---

## Meilenstein 3: GitHub Secrets konfigurieren

**Auf GitHub:**
1. Settings → Secrets and variables → Actions
2. **New repository secret**

**Secrets hinzufügen:**

| Name | Wert | Beispiel |
|------|-------|----------|
| `CML_HOST` | Ihre CML-URL | `https://xxx.xxx.xxx.xxx` |
| `CML_USERNAME` | CML Username | `IhrUsername` |
| `CML_PASSWORD` | CML Password | `IhrPassword` |

---

## Meilenstein 4: GitHub Actions committen

```bash
cd ~/cml-as-code-ansible

git add .github/

git commit -m "Add CI/CD pipeline"

git push origin test
```

**Auf GitHub beobachten:** 

1. Gehen Sie zu **Actions** Tab
2. Sie sollten sehen: **"Starte das Test-Netzwerk in CML"**
3. Der Workflow läuft automatisch

---

![line](images/banner.png)
<p align="center">
<a href="Teil06_pyATS_Test_erstellen.md"><img src="images/previous.png" width="150px"></a>
<a href="Teil08_Produktiv-Netz_bereitstellen_Deployment.md"><img src="images/next.png" width="150px"></a>
</p>