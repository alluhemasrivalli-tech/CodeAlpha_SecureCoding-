#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║   VULNERABLE APPLICATION — FOR SECURITY AUDIT PURPOSES ONLY ║
║   CodeAlpha Cybersecurity Internship — Task 3                ║
║   DO NOT USE IN PRODUCTION                                   ║
╚══════════════════════════════════════════════════════════════╝

This file intentionally contains common security vulnerabilities
for the purpose of demonstrating a Secure Code Review.
"""

import sqlite3
import os
import subprocess
import pickle
import hashlib

# ─────────────────────────────────────────────────────────────
# VULNERABILITY 1: Hardcoded Credentials (CWE-798)
# ─────────────────────────────────────────────────────────────
DB_PASSWORD = "admin123"          # VULN: hardcoded password
SECRET_KEY  = "mysecretkey"       # VULN: hardcoded secret key
API_KEY     = "12345-abcde-key"   # VULN: hardcoded API key


# ─────────────────────────────────────────────────────────────
# VULNERABILITY 2: SQL Injection (CWE-89)
# ─────────────────────────────────────────────────────────────
def get_user(username):
    """Fetch user from database — VULNERABLE to SQL Injection."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # VULN: Direct string concatenation — allows SQL injection
    # Attack: username = "' OR '1'='1" → returns ALL users
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()


def login(username, password):
    """Login function — VULNERABLE to SQL Injection."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # VULN: SQL Injection via string formatting
    query = "SELECT * FROM users WHERE username='%s' AND password='%s'" % (username, password)
    cursor.execute(query)
    user = cursor.fetchone()
    return user is not None


# ─────────────────────────────────────────────────────────────
# VULNERABILITY 3: Command Injection (CWE-78)
# ─────────────────────────────────────────────────────────────
def ping_host(host):
    """Ping a host — VULNERABLE to Command Injection."""
    # VULN: User input passed directly to shell
    # Attack: host = "google.com; rm -rf /"
    command = "ping -c 1 " + host
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def read_file(filename):
    """Read a file — VULNERABLE to Path Traversal (CWE-22)."""
    # VULN: No path sanitization
    # Attack: filename = "../../etc/passwd"
    with open(filename, "r") as f:
        return f.read()


# ─────────────────────────────────────────────────────────────
# VULNERABILITY 4: Weak Password Hashing (CWE-916)
# ─────────────────────────────────────────────────────────────
def hash_password(password):
    """Hash a password — VULNERABLE: uses MD5 (broken algorithm)."""
    # VULN: MD5 is cryptographically broken, no salt used
    return hashlib.md5(password.encode()).hexdigest()


def store_user(username, password):
    """Store user — VULNERABLE: weak hashing + no input validation."""
    hashed = hash_password(password)   # VULN: MD5 hash, no salt
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # VULN: SQL Injection again
    cursor.execute("INSERT INTO users VALUES ('" + username + "', '" + hashed + "')")
    conn.commit()


# ─────────────────────────────────────────────────────────────
# VULNERABILITY 5: Insecure Deserialization (CWE-502)
# ─────────────────────────────────────────────────────────────
def load_user_session(session_data):
    """Load user session — VULNERABLE to Insecure Deserialization."""
    # VULN: pickle.loads() on untrusted data allows Remote Code Execution
    return pickle.loads(session_data)


def save_user_session(user_object):
    """Save session — VULNERABLE: uses pickle."""
    return pickle.dumps(user_object)


# ─────────────────────────────────────────────────────────────
# VULNERABILITY 6: Sensitive Data Exposure (CWE-200)
# ─────────────────────────────────────────────────────────────
def process_payment(card_number, cvv, amount):
    """Process payment — VULNERABLE: logs sensitive data."""
    # VULN: Credit card details printed/logged in plaintext
    print(f"[LOG] Processing payment: card={card_number}, cvv={cvv}, amount={amount}")

    # VULN: Storing card number in plain text variable
    last_transaction = {"card": card_number, "cvv": cvv, "amount": amount}
    return last_transaction


# ─────────────────────────────────────────────────────────────
# VULNERABILITY 7: Missing Input Validation (CWE-20)
# ─────────────────────────────────────────────────────────────
def calculate_discount(price, discount_percent):
    """Calculate discount — VULNERABLE: no input validation."""
    # VULN: No validation — discount could be 999% (negative price)
    # VULN: No type checking — could crash with non-numeric input
    final_price = price - (price * discount_percent / 100)
    return final_price


def create_user_file(username, content):
    """Create a file — VULNERABLE: Path Traversal + no sanitization."""
    # VULN: username could be "../../etc/cron.d/malicious"
    filepath = f"users/{username}.txt"
    with open(filepath, "w") as f:
        f.write(content)


# ─────────────────────────────────────────────────────────────
# VULNERABILITY 8: Debug Mode / Information Disclosure (CWE-215)
# ─────────────────────────────────────────────────────────────
DEBUG = True   # VULN: Debug mode enabled in production code

def handle_error(e):
    """Error handler — VULNERABLE: exposes stack trace to users."""
    if DEBUG:
        # VULN: Full stack trace and internal info exposed
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc(), "db_password": DB_PASSWORD}
    return {"error": "Something went wrong"}


if __name__ == "__main__":
    print("=" * 60)
    print("  VULNERABLE APP — Security Audit Target")
    print("  CodeAlpha Internship Task 3")
    print("=" * 60)
    print("\n[!] This app contains intentional vulnerabilities.")
    print("[!] For educational/audit purposes only.\n")

    # Demo of vulnerabilities
    print("[*] Weak password hash demo:")
    print(f"    MD5('password123') = {hash_password('password123')}")

    print("\n[*] Vulnerable SQL query demo:")
    print("    Query: SELECT * FROM users WHERE username='' OR '1'='1'")
    print("    Result: Would return ALL users from database!")

    print("\n[*] Command injection demo:")
    print("    Input: 'google.com; echo INJECTED'")
    print("    Would execute: ping -c 1 google.com; echo INJECTED")
