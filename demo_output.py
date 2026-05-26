#!/usr/bin/env python3
"""
Task 3 — Secure Coding Review DEMO OUTPUT
Run: python demo_output.py
No dependencies needed!
"""

import time

R  = "\033[91m"
G  = "\033[92m"
Y  = "\033[93m"
C  = "\033[96m"
B  = "\033[94m"
M  = "\033[95m"
W  = "\033[97m"
DIM= "\033[2m"
BO = "\033[1m"
RS = "\033[0m"

def p(text, delay=0.04):
    print(text)
    time.sleep(delay)

def slow(text, delay=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def section(title):
    print()
    print(f"{BO}{Y}{'═'*62}{RS}")
    print(f"{BO}{W}  {title}{RS}")
    print(f"{BO}{Y}{'═'*62}{RS}")
    time.sleep(0.5)

def main():

    # ── PART 1: VULNERABLE APP ─────────────────────────────────
    print(f"""
{R}╔══════════════════════════════════════════════════════════════╗
║  {W}{BO}  VULNERABLE APP — Security Audit Target{RS}{R}                   ║
║  {DIM}CodeAlpha Cybersecurity Internship — Task 3{RS}{R}                 ║
╚══════════════════════════════════════════════════════════════╝{RS}
""")
    time.sleep(0.8)

    p(f"{R}[!] This app contains intentional vulnerabilities.{RS}", 0.3)
    p(f"{R}[!] For educational/audit purposes ONLY.{RS}", 0.5)

    # VUL 1
    section("🔴 VULNERABILITY 1 — Hardcoded Credentials (CWE-798)")
    time.sleep(0.3)
    p(f"{DIM}  Scanning source code for hardcoded secrets...{RS}", 0.4)
    time.sleep(0.6)
    p(f"{R}  [FOUND] Line 18 :  DB_PASSWORD = \"admin123\"          ← HARDCODED!{RS}", 0.3)
    p(f"{R}  [FOUND] Line 19 :  SECRET_KEY  = \"mysecretkey\"        ← HARDCODED!{RS}", 0.3)
    p(f"{R}  [FOUND] Line 20 :  API_KEY     = \"12345-abcde-key\"    ← HARDCODED!{RS}", 0.4)
    time.sleep(0.3)
    p(f"{Y}  ⚠  Anyone with GitHub access can steal these credentials!{RS}", 0.3)

    # VUL 2
    section("🔴 VULNERABILITY 2 — SQL Injection (CWE-89)")
    time.sleep(0.3)
    p(f"{DIM}  Scanning for unsafe SQL queries...{RS}", 0.4)
    time.sleep(0.5)
    p(f"{R}  [FOUND] Line 29 :  query = \"SELECT * FROM users WHERE username = '\" + username + \"'\"{RS}", 0.3)
    p(f"{R}  [FOUND] Line 42 :  query = \"SELECT * FROM users WHERE username='%s' AND password='%s'\" % (username, password){RS}", 0.4)
    time.sleep(0.3)
    p(f"{Y}  ⚠  Attack demo :{RS}")
    p(f"{DIM}     Input    →  username = \"' OR '1'='1' --\"{RS}", 0.2)
    p(f"{DIM}     Query    →  SELECT * FROM users WHERE username='' OR '1'='1' --'{RS}", 0.2)
    p(f"{R}     Result   →  RETURNS ALL USERS FROM DATABASE! 💀{RS}", 0.4)

    # VUL 3
    section("🔴 VULNERABILITY 3 — Command Injection (CWE-78)")
    time.sleep(0.3)
    p(f"{DIM}  Scanning for shell=True usage...{RS}", 0.4)
    time.sleep(0.5)
    p(f"{R}  [FOUND] Line 56 :  command = \"ping -c 1 \" + host{RS}", 0.2)
    p(f"{R}  [FOUND] Line 57 :  subprocess.run(command, shell=True, ...){RS}", 0.4)
    time.sleep(0.3)
    p(f"{Y}  ⚠  Attack demo :{RS}")
    p(f"{DIM}     Input    →  host = \"google.com; rm -rf /important_files\"{RS}", 0.2)
    p(f"{DIM}     Executes →  ping -c 1 google.com; rm -rf /important_files{RS}", 0.2)
    p(f"{R}     Result   →  ARBITRARY SYSTEM COMMAND EXECUTION! 💀{RS}", 0.4)

    # VUL 4
    section("🟠 VULNERABILITY 4 — Weak Password Hashing (CWE-916)")
    time.sleep(0.3)
    p(f"{DIM}  Checking password hashing algorithm...{RS}", 0.4)
    time.sleep(0.5)
    p(f"{R}  [FOUND] Line 72 :  return hashlib.md5(password.encode()).hexdigest(){RS}", 0.4)
    time.sleep(0.3)
    p(f"{Y}  ⚠  MD5 Hash Demo (crackable in seconds):{RS}")
    p(f"{DIM}     md5('password123') = {W}482c811da5d5b4bc6d497ffa98491e38{RS}", 0.2)
    p(f"{DIM}     md5('admin')       = {W}21232f297a57a5a743894a0e4a801fc3{RS}", 0.2)
    p(f"{DIM}     md5('123456')      = {W}e10adc3949ba59abbe56e057f20f883e{RS}", 0.2)
    p(f"{R}     ↑ All these are in rainbow tables — instantly crackable! 💀{RS}", 0.4)
    p(f"{R}     ↑ No salt used — same password = same hash always!{RS}", 0.3)

    # VUL 5
    section("🔴 VULNERABILITY 5 — Insecure Deserialization (CWE-502)")
    time.sleep(0.3)
    p(f"{DIM}  Scanning for pickle usage on untrusted data...{RS}", 0.4)
    time.sleep(0.5)
    p(f"{R}  [FOUND] Line 83 :  return pickle.loads(session_data)   ← REMOTE CODE EXECUTION RISK!{RS}", 0.4)
    time.sleep(0.3)
    p(f"{Y}  ⚠  An attacker can craft a malicious pickle payload{RS}", 0.2)
    p(f"{R}     that executes ANY command on your server when loaded! 💀{RS}", 0.4)

    # VUL 6
    section("🟠 VULNERABILITY 6 — Sensitive Data Exposure (CWE-200)")
    time.sleep(0.3)
    p(f"{DIM}  Scanning for sensitive data in logs...{RS}", 0.4)
    time.sleep(0.5)
    p(f"{R}  [FOUND] Line 95 :  print(f\"[LOG] Processing payment: card={{card_number}}, cvv={{cvv}}\"){RS}", 0.4)
    time.sleep(0.3)
    p(f"{Y}  ⚠  Simulated log output :{RS}")
    p(f"{R}     [LOG] Processing payment: card=4111111111111234, cvv=789, amount=5000{RS}", 0.3)
    p(f"{R}     ↑ Full credit card + CVV printed in plain text logs! 💀{RS}", 0.4)

    # VUL 7 & 8
    section("🟡 VULNERABILITY 7 — Missing Input Validation (CWE-20)")
    time.sleep(0.3)
    p(f"{DIM}  Checking input validation...{RS}", 0.4)
    time.sleep(0.5)
    p(f"{R}  [FOUND] Line 103 : No type/range check on discount_percent{RS}", 0.3)
    p(f"{Y}  ⚠  discount_percent=999  →  final_price = -49900.0  (negative price!){RS}", 0.4)

    section("🟢 VULNERABILITY 8 — Debug Mode Enabled (CWE-215)")
    time.sleep(0.3)
    p(f"{R}  [FOUND] Line 115 : DEBUG = True  ← Hardcoded ON{RS}", 0.3)
    p(f"{R}  [FOUND] Line 119 : returns traceback + db_password to user!{RS}", 0.4)

    # Summary table
    print()
    print(f"{BO}{R}{'═'*62}{RS}")
    print(f"{BO}{W}  📊 AUDIT SUMMARY — vulnerable_app.py{RS}")
    print(f"{BO}{R}{'═'*62}{RS}")
    time.sleep(0.3)
    rows = [
        (R, "CRITICAL", "SQL Injection",              "CWE-89",  "A03"),
        (R, "CRITICAL", "Command Injection",           "CWE-78",  "A03"),
        (R, "CRITICAL", "Insecure Deserialization",    "CWE-502", "A08"),
        (M, "HIGH    ", "Hardcoded Credentials",       "CWE-798", "A07"),
        (M, "HIGH    ", "Weak Password Hashing (MD5)", "CWE-916", "A07"),
        (M, "HIGH    ", "Sensitive Data Exposure",     "CWE-200", "A02"),
        (Y, "MEDIUM  ", "Missing Input Validation",    "CWE-20",  "A03"),
        (G, "LOW     ", "Debug Mode / Info Disclosure","CWE-215", "A05"),
    ]
    for color, sev, name, cwe, owasp in rows:
        p(f"  {color}[{sev}]{RS}  {W}{name:<30}{RS}  {DIM}{cwe}  OWASP {owasp}{RS}", 0.15)

    print()
    p(f"{R}{BO}  Total Vulnerabilities Found : 8{RS}", 0.3)
    p(f"{R}  Critical : 3   High : 3   Medium : 1   Low : 1{RS}", 0.5)

    # ── PART 2: SECURE APP ────────────────────────────────────
    time.sleep(1)
    print(f"""
{G}╔══════════════════════════════════════════════════════════════╗
║  {W}{BO}  SECURE APP — All Vulnerabilities Fixed ✅{RS}{G}                 ║
║  {DIM}CodeAlpha Cybersecurity Internship — Task 3{RS}{G}                 ║
╚══════════════════════════════════════════════════════════════╝{RS}
""")
    time.sleep(0.5)

    fixes = [
        ("SQL Injection",              "Parameterized queries — user input never touches SQL string"),
        ("Command Injection",          "subprocess list args + regex validation — no shell=True"),
        ("Insecure Deserialization",   "Replaced pickle with JSON — cannot execute arbitrary code"),
        ("Hardcoded Credentials",      "Environment variables — os.environ.get('SECRET_KEY')"),
        ("Weak MD5 Hashing",           "PBKDF2-HMAC-SHA256 + random salt — 260,000 iterations"),
        ("Sensitive Data Exposure",    "Masked card number in logs — CVV never stored or logged"),
        ("Missing Input Validation",   "Type checks + range validation on all inputs"),
        ("Debug Mode",                 "DEBUG=os.environ.get('DEBUG','false') — env controlled"),
    ]

    for name, fix in fixes:
        p(f"  {G}[✓] {W}{name:<30}{RS}  {DIM}{fix}{RS}", 0.25)

    time.sleep(0.5)
    print()
    print(f"{DIM}  Demonstrating secure password hashing...{RS}")
    time.sleep(0.8)

    import hashlib, secrets
    for i in range(3):
        salt = secrets.token_hex(16)
        key  = hashlib.pbkdf2_hmac('sha256', b'password123', salt.encode(), 260000)
        p(f"  {G}Run {i+1}:{RS}  Hash={W}{key.hex()[:32]}...{RS}  Salt={DIM}{salt[:16]}...{RS}", 0.2)

    print()
    p(f"{G}{BO}  ↑ Every run = different hash (salt working correctly!) ✅{RS}", 0.3)

    # Final
    time.sleep(0.5)
    print()
    print(f"{BO}{G}{'═'*62}{RS}")
    print(f"{BO}{W}  ✅ Secure Code Review Complete!{RS}")
    print(f"{BO}{G}{'═'*62}{RS}")
    p(f"  {G}8 vulnerabilities identified and fixed{RS}", 0.2)
    p(f"  {G}Full report saved in SECURITY_AUDIT_REPORT.md{RS}", 0.2)
    p(f"  {G}Secure version in secure_app.py{RS}", 0.3)
    print()

if __name__ == "__main__":
    main()
