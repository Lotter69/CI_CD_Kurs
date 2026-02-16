## Teil 8: Produktiv-Netz Bereitstellen (Deployment)
![line](images/banner.png)
### Schritt 32: Pull Request & Merge

**Auf GitHub:**

1. Pull requests → New pull request
2. Base: main ← Compare: test
3. Create pull request
4. Titel: "Initial setup"
5. Beschreibung:
```
Initiale Konfiguration des Produktiv-Netzes mit Ansible-kodierter Konfiguration
```
6. Warten bis alle Checks grün
7. **Merge pull request**

**Nach dem Merge startet:**
- Job: **"Bereitstellung für reales Netz"**

### Schritt 33: Produktiv-Netz verifizieren

```bash
ssh YoursshUsermane@xxx.xxx.xxx.xxx  # Ihre Prod-Router1 IP
enable
show ip access-lists 110
show ip interface Ethernet0/1 | include access list
```

**Erwartete Ausgabe:**
```
Extended IP access list 110
    20 deny tcp any any eq www
    40 permit ip any any
    
Inbound  access list is 110
```

---

![line](../images/banner.png)
<p align="center">
<a href="../01-why-automation/1.md"><img src="images/previous.png" width="150px"></a>
<a href="../02-intro-to-apis/1.md"><img src="images/next.png" width="150px"></a>
</p>