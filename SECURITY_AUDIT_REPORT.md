# 🔐 Secure Code Review Report
## CodeAlpha Cybersecurity Internship — Task 3

**Application Audited:** `vulnerable_app.py` (Python Web Application)
**Reviewed By:** [Your Name]
**Date:** May 2025
**Severity Scale:** 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low

---

## 📋 Executive Summary

A thorough security code review was performed on `vulnerable_app.py`, a Python application simulating a user authentication and payment system. The audit identified **8 security vulnerabilities** across multiple OWASP Top 10 categories.

| Severity | Count |
|----------|-------|
| 🔴 Critical | 3 |
| 🟠 High | 3 |
| 🟡 Medium | 1 |
| 🟢 Low | 1 |
| **Total** | **8** |

---

## 🔍 Vulnerability Findings

---

### VUL-001 — SQL Injection
**Severity:** 🔴 Critical
**CWE:** CWE-89
**OWASP:** A03:2021 – Injection

**Vulnerable Code:**
```python
# VULNERABLE
query = "SELECT * FROM users WHERE username = '" + username + "'"
cursor.execute(query)
```

**Attack Example:**
```
username = "' OR '1'='1' --"
→ Returns ALL users from the database
```

**Impact:** Full database compromise, authentication bypass, data theft.

**Fixed Code:**
```python
# SECURE — Parameterized query
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

**Remediation:** Always use parameterized queries or prepared statements. Never concatenate user input into SQL strings.

---

### VUL-002 — Command Injection
**Severity:** 🔴 Critical
**CWE:** CWE-78
**OWASP:** A03:2021 – Injection

**Vulnerable Code:**
```python
# VULNERABLE
command = "ping -c 1 " + host
result = subprocess.run(command, shell=True, ...)
```

**Attack Example:**
```
host = "google.com; rm -rf /important_files"
→ Executes arbitrary system commands
```

**Impact:** Full system compromise, data destruction, remote code execution.

**Fixed Code:**
```python
# SECURE — List args, no shell=True, input validation
if not re.match(r'^[a-zA-Z0-9.\-]{1,253}$', host):
    return "Error: Invalid hostname"
subprocess.run(["ping", "-c", "1", host], shell=False)
```

**Remediation:** Never use `shell=True` with user input. Pass arguments as a list. Validate all input with strict regex.

---

### VUL-003 — Insecure Deserialization
**Severity:** 🔴 Critical
**CWE:** CWE-502
**OWASP:** A08:2021 – Software and Data Integrity Failures

**Vulnerable Code:**
```python
# VULNERABLE
def load_user_session(session_data):
    return pickle.loads(session_data)  # RCE possible!
```

**Attack Example:**
```python
# Malicious pickle payload executes system commands on load
import os, pickle
payload = pickle.dumps(type('X', (), {'__reduce__': lambda s: (os.system, ('rm -rf /',))})())
load_user_session(payload)  # → Executes rm -rf /
```

**Impact:** Remote Code Execution (RCE) — complete server takeover.

**Fixed Code:**
```python
# SECURE — Use JSON instead of pickle
def load_user_session(session_data: str) -> dict:
    return json.loads(session_data)
```

**Remediation:** Never deserialize untrusted data with `pickle`. Use JSON for session data.

---

### VUL-004 — Hardcoded Credentials
**Severity:** 🟠 High
**CWE:** CWE-798
**OWASP:** A07:2021 – Identification and Authentication Failures

**Vulnerable Code:**
```python
# VULNERABLE
DB_PASSWORD = "admin123"
SECRET_KEY  = "mysecretkey"
API_KEY     = "12345-abcde-key"
```

**Impact:** Anyone with code access (GitHub leak, insider threat) has full credential access.

**Fixed Code:**
```python
# SECURE — Environment variables
DB_PASSWORD = os.environ.get("DB_PASSWORD")
SECRET_KEY  = os.environ.get("SECRET_KEY")
```

**Remediation:** Store all secrets in environment variables or a secrets manager (AWS Secrets Manager, HashiCorp Vault). Never commit credentials to version control.

---

### VUL-005 — Weak Password Hashing
**Severity:** 🟠 High
**CWE:** CWE-916
**OWASP:** A07:2021 – Identification and Authentication Failures

**Vulnerable Code:**
```python
# VULNERABLE — MD5 is broken, no salt
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
```

**Why It's Dangerous:**
- MD5 is cryptographically broken
- No salt → vulnerable to rainbow table attacks
- `md5("password123")` = `482c811da5d5b4bc6d497ffa98491e38` → crackable in seconds

**Fixed Code:**
```python
# SECURE — PBKDF2 with random salt, 260,000 iterations
salt = secrets.token_hex(32)
key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 260000)
```

**Remediation:** Use bcrypt, Argon2, or PBKDF2 with a random salt. Never use MD5 or SHA1 for passwords.

---

### VUL-006 — Sensitive Data Exposure
**Severity:** 🟠 High
**CWE:** CWE-200
**OWASP:** A02:2021 – Cryptographic Failures

**Vulnerable Code:**
```python
# VULNERABLE — Logs full credit card and CVV
print(f"[LOG] Processing payment: card={card_number}, cvv={cvv}")
last_transaction = {"card": card_number, "cvv": cvv}
```

**Impact:** Credit card data in logs, memory dumps, or crash reports.

**Fixed Code:**
```python
# SECURE — Mask card, never log CVV
masked_card = "**** **** **** " + card_number[-4:]
logger.info(f"Processing payment: card={masked_card}, amount={amount}")
```

**Remediation:** Never log sensitive data. Mask card numbers. Never store CVV. Follow PCI-DSS standards.

---

### VUL-007 — Missing Input Validation
**Severity:** 🟡 Medium
**CWE:** CWE-20
**OWASP:** A03:2021 – Injection

**Vulnerable Code:**
```python
# VULNERABLE — No validation
def calculate_discount(price, discount_percent):
    final_price = price - (price * discount_percent / 100)
    return final_price
```

**Attack Example:**
```
discount_percent = 999 → negative price
price = "abc"          → crashes application
```

**Fixed Code:**
```python
# SECURE — Full validation
if not isinstance(price, (int, float)):
    raise TypeError("Price must be a number")
if not (0 <= discount_percent <= 100):
    raise ValueError("Discount must be between 0 and 100")
```

**Remediation:** Validate all inputs — type, range, format, and length.

---

### VUL-008 — Debug Mode & Information Disclosure
**Severity:** 🟢 Low
**CWE:** CWE-215
**OWASP:** A05:2021 – Security Misconfiguration

**Vulnerable Code:**
```python
# VULNERABLE
DEBUG = True  # Hardcoded ON

def handle_error(e):
    if DEBUG:
        return {"error": str(e), "traceback": traceback.format_exc(), "db_password": DB_PASSWORD}
```

**Impact:** Stack traces, file paths, and secrets exposed to attackers in error responses.

**Fixed Code:**
```python
# SECURE
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

def handle_error(e):
    logger.error(f"Internal error: {e}", exc_info=True)  # Log server-side only
    return {"error": "An internal error occurred."}       # Generic to user
```

**Remediation:** Never hardcode DEBUG=True. Log errors server-side. Return generic error messages to users.

---

## 📊 Vulnerability Summary Table

| ID | Vulnerability | Severity | CWE | OWASP Category | Status |
|----|--------------|----------|-----|----------------|--------|
| VUL-001 | SQL Injection | 🔴 Critical | CWE-89 | A03 Injection | ✅ Fixed |
| VUL-002 | Command Injection | 🔴 Critical | CWE-78 | A03 Injection | ✅ Fixed |
| VUL-003 | Insecure Deserialization | 🔴 Critical | CWE-502 | A08 Integrity | ✅ Fixed |
| VUL-004 | Hardcoded Credentials | 🟠 High | CWE-798 | A07 Auth | ✅ Fixed |
| VUL-005 | Weak Password Hashing | 🟠 High | CWE-916 | A07 Auth | ✅ Fixed |
| VUL-006 | Sensitive Data Exposure | 🟠 High | CWE-200 | A02 Crypto | ✅ Fixed |
| VUL-007 | Missing Input Validation | 🟡 Medium | CWE-20 | A03 Injection | ✅ Fixed |
| VUL-008 | Debug Mode / Info Disclosure | 🟢 Low | CWE-215 | A05 Misconfig | ✅ Fixed |

---

## ✅ Secure Coding Best Practices Applied

1. **Never trust user input** — validate everything
2. **Use parameterized queries** — prevent SQL injection
3. **Avoid shell=True** — prevent command injection
4. **Use JSON over pickle** — prevent deserialization attacks
5. **Store secrets in environment variables** — no hardcoding
6. **Use strong hashing (PBKDF2/bcrypt)** — protect passwords
7. **Never log sensitive data** — protect user privacy
8. **Disable debug in production** — prevent info disclosure

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| Manual Code Review | Primary vulnerability identification |
| Bandit (Python) | Static analysis for common security issues |
| OWASP Guidelines | Vulnerability classification reference |
| CWE Database | Common Weakness Enumeration reference |

---

## 📚 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [Python Security Best Practices](https://snyk.io/blog/python-security-best-practices/)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/)

---

*Report prepared by [Your Name] | CodeAlpha Cybersecurity Internship | Task 3 — Secure Coding Review*
