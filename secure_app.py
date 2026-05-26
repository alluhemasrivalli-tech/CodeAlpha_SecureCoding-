#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║   SECURE VERSION — All Vulnerabilities Fixed                 ║
║   CodeAlpha Cybersecurity Internship — Task 3                ║
╚══════════════════════════════════════════════════════════════╝

This is the remediated, secure version of vulnerable_app.py.
All 8 vulnerabilities have been fixed following OWASP best practices.
"""

import sqlite3
import os
import subprocess
import json
import hashlib
import hmac
import secrets
import re
import logging
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# FIX 1: No Hardcoded Credentials — Use Environment Variables
# ─────────────────────────────────────────────────────────────
DB_PASSWORD = os.environ.get("DB_PASSWORD")           # ✅ From env
SECRET_KEY  = os.environ.get("SECRET_KEY")            # ✅ From env
API_KEY     = os.environ.get("API_KEY")               # ✅ From env

if not SECRET_KEY:
    raise EnvironmentError("SECRET_KEY environment variable is not set!")


# ─────────────────────────────────────────────────────────────
# FIX 2: SQL Injection — Use Parameterized Queries
# ─────────────────────────────────────────────────────────────
def get_user(username: str):
    """Fetch user — SECURE: uses parameterized query."""
    if not username or len(username) > 50:
        return None
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # ✅ Parameterized query — user input never touches SQL string
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()


def login(username: str, password: str) -> bool:
    """Login function — SECURE: parameterized query + proper password check."""
    if not username or not password:
        return False
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # ✅ Parameterized query
    cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if not row:
        return False
    stored_hash, salt = row
    # ✅ Verify using constant-time comparison
    return hmac.compare_digest(stored_hash, hash_password(password, salt))


# ─────────────────────────────────────────────────────────────
# FIX 3: Command Injection — Use subprocess with list args
# ─────────────────────────────────────────────────────────────
def ping_host(host: str) -> str:
    """Ping a host — SECURE: no shell=True, validated input."""
    # ✅ Validate host with regex — only allow valid hostnames/IPs
    if not re.match(r'^[a-zA-Z0-9.\-]{1,253}$', host):
        return "Error: Invalid hostname"
    # ✅ Pass as list — shell=False by default, no injection possible
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True, text=True, timeout=5
    )
    return result.stdout


def read_file(filename: str) -> str:
    """Read a file — SECURE: Path Traversal prevention."""
    # ✅ Resolve to safe base directory
    base_dir = Path("/safe/files/directory").resolve()
    requested = (base_dir / filename).resolve()
    # ✅ Ensure path stays within base directory
    if not str(requested).startswith(str(base_dir)):
        raise PermissionError("Access denied: Path traversal attempt detected")
    with open(requested, "r") as f:
        return f.read()


# ─────────────────────────────────────────────────────────────
# FIX 4: Strong Password Hashing — bcrypt / PBKDF2 with salt
# ─────────────────────────────────────────────────────────────
def hash_password(password: str, salt: str = None) -> tuple:
    """Hash password — SECURE: PBKDF2 with random salt."""
    if salt is None:
        # ✅ Generate cryptographically secure random salt
        salt = secrets.token_hex(32)
    # ✅ PBKDF2-HMAC-SHA256 with 260,000 iterations (OWASP recommended)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        260000
    )
    return key.hex(), salt


def store_user(username: str, password: str):
    """Store user — SECURE: strong hashing + input validation."""
    # ✅ Input validation
    if not username or not re.match(r'^[a-zA-Z0-9_]{3,30}$', username):
        raise ValueError("Invalid username format")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")

    password_hash, salt = hash_password(password)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # ✅ Parameterized query
    cursor.execute(
        "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
        (username, password_hash, salt)
    )
    conn.commit()


# ─────────────────────────────────────────────────────────────
# FIX 5: Insecure Deserialization — Use JSON instead of pickle
# ─────────────────────────────────────────────────────────────
def load_user_session(session_data: str) -> dict:
    """Load session — SECURE: uses JSON, not pickle."""
    # ✅ JSON is safe — cannot execute arbitrary code
    try:
        data = json.loads(session_data)
        # ✅ Validate expected fields exist
        if not isinstance(data, dict) or "user_id" not in data:
            raise ValueError("Invalid session format")
        return data
    except json.JSONDecodeError:
        raise ValueError("Corrupted session data")


def save_user_session(user_dict: dict) -> str:
    """Save session — SECURE: JSON serialization."""
    # ✅ Only serialize safe, known fields
    safe_data = {
        "user_id": user_dict.get("user_id"),
        "username": user_dict.get("username"),
        "role": user_dict.get("role", "user")
    }
    return json.dumps(safe_data)


# ─────────────────────────────────────────────────────────────
# FIX 6: No Sensitive Data in Logs
# ─────────────────────────────────────────────────────────────

# ✅ Configure proper logging (not print statements)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def process_payment(card_number: str, cvv: str, amount: float) -> dict:
    """Process payment — SECURE: never log sensitive data."""
    # ✅ Only log masked card number, never CVV or full card
    masked_card = "**** **** **** " + card_number[-4:]
    logger.info(f"Processing payment: card={masked_card}, amount={amount}")
    # ✅ Never store raw card/CVV in variables or logs
    return {"status": "processed", "card_last4": card_number[-4:], "amount": amount}


# ─────────────────────────────────────────────────────────────
# FIX 7: Input Validation
# ─────────────────────────────────────────────────────────────
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discount — SECURE: full input validation."""
    # ✅ Type checking
    if not isinstance(price, (int, float)) or not isinstance(discount_percent, (int, float)):
        raise TypeError("Price and discount must be numbers")
    # ✅ Range validation
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not (0 <= discount_percent <= 100):
        raise ValueError("Discount must be between 0 and 100")
    return round(price - (price * discount_percent / 100), 2)


def create_user_file(username: str, content: str):
    """Create file — SECURE: sanitized filename."""
    # ✅ Strict username validation — no path characters allowed
    if not re.match(r'^[a-zA-Z0-9_]{1,30}$', username):
        raise ValueError("Invalid username for file creation")
    # ✅ Safe base directory + resolved path check
    base_dir = Path("users").resolve()
    filepath = (base_dir / f"{username}.txt").resolve()
    if not str(filepath).startswith(str(base_dir)):
        raise PermissionError("Path traversal detected")
    with open(filepath, "w") as f:
        f.write(content)


# ─────────────────────────────────────────────────────────────
# FIX 8: No Debug Mode in Production — Safe Error Handling
# ─────────────────────────────────────────────────────────────
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"   # ✅ From env only

def handle_error(e: Exception) -> dict:
    """Error handler — SECURE: never expose internals."""
    # ✅ Log full error server-side only
    logger.error(f"Internal error: {e}", exc_info=True)
    # ✅ Return generic message to user — no stack traces, no secrets
    return {"error": "An internal error occurred. Please try again."}


if __name__ == "__main__":
    print("=" * 60)
    print("  SECURE APP — All Vulnerabilities Fixed")
    print("  CodeAlpha Internship Task 3")
    print("=" * 60)
    print("\n[✓] Parameterized queries — SQL Injection prevented")
    print("[✓] PBKDF2+salt — Weak hashing fixed")
    print("[✓] subprocess list args — Command injection prevented")
    print("[✓] JSON sessions — Insecure deserialization fixed")
    print("[✓] Environment variables — Hardcoded credentials removed")
    print("[✓] Input validation — Missing validation fixed")
    print("[✓] Masked logging — Sensitive data exposure fixed")
    print("[✓] Debug mode off — Info disclosure fixed\n")

    # Demo secure password hashing
    pw_hash, salt = hash_password("password123")
    print(f"[*] PBKDF2 hash demo:")
    print(f"    Hash : {pw_hash[:40]}...")
    print(f"    Salt : {salt[:20]}...")
    print(f"    (Each run produces different hash — salt works!)")
