# **Identity Governance & Entra ID Security Engine**

Recapture a share of the [$30B lost annually](https://ramp.com/blog/unused-software-subscriptions) to 'ghost' licenses by automating the detection of stale, over-privileged, and leak-prone accounts. 

---
![](./assets/hero.png)
## **Overview**

A lightweight Python automation utility that scans Entra ID account data, highlights stale or misconfigured accounts, and generates a ready-to-use PowerShell remediation script. Enterprise-ready, and designed for rapid audits (access reviews), security hygiene, and improving offboarding completeness. 

---

## **Features**

* Detects:

  * **Stale accounts** (enabled but inactive for X days)
  * **Disabled users with active licenses**
  * **Accounts requiring manual review**
* Assigns **severity levels** for prioritization
* Generates:

  * `discrepancies.csv` : full audit results
  * `remediation.ps1` : PowerShell disable commands
* Includes **dry-run mode** for safe preview
* Works with **CSV AD exports** or can be extended to LDAP/MS Graph

---

## **Sample Use Cases**

* Pre-offboarding cleanup
* Quarterly AD hygiene audits
* License optimization
* Security posture hardening
* Validating HR → IT sync accuracy

---

## **Installation**

### **Requirements**

* Python 3.8+
* `pandas`
* `python-dateutil`

### **Install packages**

```bash
pip install pandas python-dateutil
```

---

## **Usage**

### **Run the audit**

```bash
python audit_ad.py --input sample_ad_export.csv
```

### **Preview commands (dry-run)**

```bash
python audit_ad.py --input sample_ad_export.csv --dry-run
```

### **Set a custom stale threshold**

```bash
python audit_ad.py --input sample_ad_export.csv --days-stale 120
```

### **Specify output directory**

```bash
python audit_ad.py --input sample_ad_export.csv --output-dir results/
```

---

## **Output Files**

### **1. discrepancies.csv**

Contains all flagged accounts, sorted by severity.
Columns include:

* `sAMAccountName`
* `displayName`
* `enabled`
* `stale`
* `licenseAssigned`
* `severity`

### **2. remediation.ps1**

PowerShell actions generated for each flagged user, for example:

```powershell
Disable-ADAccount -Identity "jdoe"  # severity=2
Disable-ADAccount -Identity "asmith"  # severity=3
```

When running with `--dry-run`, commands are output as `echo` instead of executed.

---

## **How Severity Is Assigned**

| Severity         | Description                                          |
| ---------------- | ---------------------------------------------------- |
| **3 (Critical)** | Disabled account still assigned licenses             |
| **2 (High)**     | Enabled but stale (inactive for X days)              |
| **1 (Low)**      | Informational or review-needed accounts (extendable) |

---

## **File Structure**

```
/
├── audit_ad.py
├── sample_ad_export.csv
├── remediation.ps1
└── README.md
```

An `out/` directory will be created automatically during execution.

---

## **Extending This Tool**

The script is intentionally minimal for rapid execution. Possible enhancements:

* **Privileged group analysis**
  Flag Domain Admins, Enterprise Admins, and IT Admins that haven’t logged in recently.

* **Microsoft Graph API integration**
  Automate license removal or account verification.

* **Ticketing system integration**
  Auto-create tickets for high-severity findings.

* **Scheduled weekly reports**
  Run through Task Scheduler or cron.

---

## **Why This Tool Is Useful**

* Reduces licensing waste
* Improves offboarding completeness
* Strengthens security posture
* Highlights gaps between HR and AD
* Saves time during audits
