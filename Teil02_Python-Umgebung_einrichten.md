## Teil 2: Python-Umgebung einrichten
![line](images/banner.png)
### Schritt 7: Virtual Environment erstellen

```bash
cd ~/cml-as-code-ansible

python3.8 -m venv venv

source venv/bin/activate
```

**Sie sollten sehen:** `(venv)` vor Ihrem Prompt

### Schritt 8: Python-Dependencies definieren

```bash
mkdir python
cd python
nano requirements.txt
```

**Inhalt von `requirements.txt`:**
```
ansible==2.13.13
pyats==24.11
genie==24.11
virl2-client==2.8.0
paramiko==3.5.0
```

**Speichern:** `Strg+O`, `Enter`, `Strg+X`

### Schritt 9: Dependencies installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verifizieren:**
```bash
ansible --version
python -c "from virl2_client import ClientLibrary; print('virl2-client OK')"
```

---
![line](images/banner.png)
<p align="center">
<a href="../01-why-automation/1.md"><img src="images/previous.png" width="150px"></a>
<a href="../02-intro-to-apis/1.md"><img src="images/next.png" width="150px"></a>
</p>