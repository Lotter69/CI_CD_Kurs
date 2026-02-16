
## Teil 1: Entwicklungsumgebung einrichten
![line](images/banner.png)
### Schritt 1: System-Pakete installieren

```bash
# Terminal öffnen
sudo apt update
sudo apt upgrade -y

# Python 3.8 (diese Version für pyATS)
sudo apt install python3.8 python3.8-venv python3.8-dev -y

# Build-Tools
sudo apt install build-essential libssl-dev libffi-dev -y

# Git
sudo apt install git -y

# SSH-Client
sudo apt install openssh-client -y

# Verifizieren
python3.8 --version
git --version
```

### Schritt 2: Git konfigurieren

```bash
git config --global user.name "Ihr Name"
git config --global user.email "ihre.email@example.com"
```

### Schritt 3: GitHub-Repository erstellen

**Auf GitHub:**
1. **+** → **New repository**
2. Name: `cml-as-code-ansible`
3. - Add README
4. - Add .gitignore: Python
5. Create repository

### Schritt 4: SSH-Key erstellen und zu GitHub hinzufügen

#### SSH-Key erstellen (Ed25519 - moderner Standard)
ssh-keygen -t ed25519 -C "ihre.email@example.com"

#### Bei den Fragen:
- Enter file in which to save the key: [Enter] (Standard: ~/.ssh/id_ed25519)
- Enter passphrase: [Enter] oder ein Passwort (empfohlen!)
- Enter same passphrase again: [Enter] oder Passwort wiederholen

**Erwartete Ausgabe:**
```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/michael/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/michael/.ssh/id_ed25519
Your public key has been saved in /home/michael/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:abcdef1234567890... ihre.email@example.com
```

> **Tipp:** Wenn Sie bereits einen SSH-Key haben, können Sie diesen wiederverwenden!

#### **4.2: Public Key anzeigen**

```bash
# Public Key anzeigen
cat ~/.ssh/id_ed25519.pub
```

**Kopieren Sie die komplette Ausgabe!** Sie sollte beginnen mit:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... ihre.email@example.com
```

#### **4.3: SSH-Key zu GitHub hinzufügen**

**Auf GitHub:**

1. Klicken Sie oben rechts auf Ihr **Profilbild** → **Settings**
2. Links: **SSH and GPG keys**
3. Klicken Sie **New SSH key**
4. **Title:** z.B. "Linux Mint - CML Lab"
5. **Key type:** Authentication Key
6. **Key:** Fügen Sie den kopierten Public Key ein
7. Klicken Sie **Add SSH key**
8. Bestätigen Sie ggf. mit Ihrem GitHub-Passwort

#### **4.4: SSH-Verbindung zu GitHub testen**

```bash
# GitHub SSH-Verbindung testen
ssh -T git@github.com
```

**Beim ersten Mal erscheint:**
```
The authenticity of host 'github.com (...)' can't be established.
...
Are you sure you want to continue connecting (yes/no/[fingerprint])? 
```

**Antworten Sie:** `yes`

**Erwartete Ausgabe:**
```
Hi IHREN-USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```
---

### Schritt 5: Repository klonen (mit SSH!)

```bash
cd ~

# Repository klonen mit SSH URL (NICHT HTTPS!)
git clone git@github.com:IHREN-USERNAME/cml-as-code-ansible.git

cd cml-as-code-ansible
git status
```

> **Wichtig:** Die URL beginnt mit `git@github.com:` (SSH) statt `https://github.com/` (HTTPS)!

**Falls Sie bereits mit HTTPS geklont haben:**
```bash
cd ~/cml-as-code-ansible

# Remote URL auf SSH umstellen
git remote set-url origin git@github.com:IHREN-USERNAME/cml-as-code-ansible.git

# Verifizieren
git remote -v
# Sollte zeigen: git@github.com:IHREN-USERNAME/cml-as-code-ansible.git
```

---


![line](../images/banner.png)
<p align="center">
<a href="../01-why-automation/1.md"><img src="images/previous.png" width="150px"></a>
<a href="../02-intro-to-apis/1.md"><img src="images/next.png" width="150px"></a>
</p>