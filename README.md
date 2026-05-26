# 🔐 Secure Coding Review — CodeAlpha Cybersecurity Internship Task 3

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Security](https://img.shields.io/badge/OWASP-Top%2010-red)
![CodeAlpha](https://img.shields.io/badge/CodeAlpha-Cybersecurity%20Intern-orange)
![Status](https://img.shields.io/badge/Vulnerabilities-8%20Fixed-green)

> A complete security code review of a vulnerable Python application identifying **8 vulnerabilities** and providing fully remediated secure code. Built as **Task 3** of the CodeAlpha Cybersecurity Internship.

---

## 📂 Project Files

| File | Description |
|------|-------------|
| `vulnerable_app.py` | Original app with 8 intentional vulnerabilities |
| `secure_app.py` | Fully remediated secure version |
| `SECURITY_AUDIT_REPORT.md` | Complete audit report with findings & fixes |

---

## 🚨 Vulnerabilities Found & Fixed

| # | Vulnerability | Severity | Fixed |
|---|--------------|----------|-------|
| 1 | SQL Injection | 🔴 Critical | ✅ |
| 2 | Command Injection | 🔴 Critical | ✅ |
| 3 | Insecure Deserialization | 🔴 Critical | ✅ |
| 4 | Hardcoded Credentials | 🟠 High | ✅ |
| 5 | Weak Password Hashing (MD5) | 🟠 High | ✅ |
| 6 | Sensitive Data Exposure | 🟠 High | ✅ |
| 7 | Missing Input Validation | 🟡 Medium | ✅ |
| 8 | Debug Mode / Info Disclosure | 🟢 Low | ✅ |

---

## ▶️ How to Run

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/CodeAlpha_SecureCoding.git
cd CodeAlpha_SecureCoding

# Run vulnerable app demo
python vulnerable_app.py

# Run secure app demo
python secure_app.py
```

---

## 🧠 Key Learnings

- SQL Injection prevented with **parameterized queries**
- Command Injection prevented by avoiding **shell=True**
- RCE prevented by replacing **pickle with JSON**
- Credentials secured via **environment variables**
- Passwords secured with **PBKDF2 + salt** (not MD5)
- Sensitive data protected by **masked logging**

---

## 👤 Author

**[Your Name]** | CodeAlpha Cybersecurity Internship | Task 3

---

## 🏷️ Tags

`cybersecurity` `secure-coding` `owasp` `python` `code-review` `sql-injection` `codealpha` `internship` `penetration-testing` `appsec`
