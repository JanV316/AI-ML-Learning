"""
Personal Vault module for PassForge V7.

Provides symmetric encryption of vault secrets using Fernet (AES-128-CBC + HMAC-SHA256),
credential CRUD database operations, and vault security health analysis.
"""

import base64
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from passforge.analyzer import analyze_password
from passforge.models import get_db_connection
from passforge.security import PBKDF2_ITERATIONS


def derive_vault_key(password: str, salt_b64: str) -> bytes:
    """
    Derive a 32-byte Fernet key from the user's password and salt using PBKDF2-HMAC-SHA256.

    Args:
        password (str): Plaintext authentication password.
        salt_b64 (str): Base64-encoded user salt string.

    Returns:
        bytes: Base64 URL-safe Fernet encryption key.
    """
    salt = base64.b64decode(salt_b64)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    derived_bytes = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(derived_bytes)


def encrypt_secret(plaintext: str, key: bytes) -> str:
    """
    Encrypt a plaintext secret using Fernet.

    Args:
        plaintext (str): Secret payload string to encrypt.
        key (bytes): Derived Fernet key.

    Returns:
        str: Encrypted ciphertext string.
    """
    fernet = Fernet(key)
    encrypted_bytes = fernet.encrypt(plaintext.encode("utf-8"))
    return encrypted_bytes.decode("utf-8")


def decrypt_secret(ciphertext: str, key: bytes) -> str:
    """
    Decrypt an encrypted ciphertext string using Fernet.

    Args:
        ciphertext (str): Encrypted payload string.
        key (bytes): Derived Fernet key.

    Returns:
        str: Plaintext secret string.
    """
    fernet = Fernet(key)
    decrypted_bytes = fernet.decrypt(ciphertext.encode("utf-8"))
    return decrypted_bytes.decode("utf-8")


def add_credential(
    user_id: int,
    service_name: str,
    username_or_email: str,
    plaintext_password: str,
    key: bytes,
    url: Optional[str] = None,
    notes: Optional[str] = None,
    db_path: Optional[str] = None,
) -> int:
    """Encrypt and store a new credential item in the user's vault."""
    encrypted_pwd = encrypt_secret(plaintext_password, key)
    now = datetime.utcnow().isoformat()

    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO credentials (user_id, service_name, username_or_email, encrypted_password, url, notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            service_name,
            username_or_email,
            encrypted_pwd,
            url or "",
            notes or "",
            now,
            now,
        ),
    )
    cred_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return cred_id


def get_user_credentials(
    user_id: int, db_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve all credential records for a user (without decrypting passwords)."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, user_id, service_name, username_or_email, url, notes, created_at, updated_at
        FROM credentials
        WHERE user_id = ?
        ORDER BY service_name ASC
        """,
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()

    credentials = []
    for r in rows:
        c = dict(r)
        c["masked_password"] = "••••••••••••"
        credentials.append(c)
    return credentials


def get_credential_by_id(
    cred_id: int, user_id: int, db_path: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Retrieve a single credential record owned by user_id."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM credentials WHERE id = ? AND user_id = ?",
        (cred_id, user_id),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_credential(
    cred_id: int,
    user_id: int,
    service_name: str,
    username_or_email: str,
    key: bytes,
    plaintext_password: Optional[str] = None,
    url: Optional[str] = None,
    notes: Optional[str] = None,
    db_path: Optional[str] = None,
) -> bool:
    """Update an existing credential record."""
    existing = get_credential_by_id(cred_id, user_id, db_path)
    if not existing:
        return False

    now = datetime.utcnow().isoformat()
    encrypted_pwd = (
        encrypt_secret(plaintext_password, key)
        if plaintext_password
        else existing["encrypted_password"]
    )

    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE credentials
        SET service_name = ?, username_or_email = ?, encrypted_password = ?, url = ?, notes = ?, updated_at = ?
        WHERE id = ? AND user_id = ?
        """,
        (
            service_name,
            username_or_email,
            encrypted_pwd,
            url or "",
            notes or "",
            now,
            cred_id,
            user_id,
        ),
    )
    conn.commit()
    conn.close()
    return True


def delete_credential(
    cred_id: int, user_id: int, db_path: Optional[str] = None
) -> bool:
    """Delete a credential record owned by user_id."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM credentials WHERE id = ? AND user_id = ?",
        (cred_id, user_id),
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def analyze_user_vault(
    user_id: int, key: bytes, db_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform a security health analysis across a user's vault items.

    Calculates metrics for total credentials, strong, moderate, weak counts,
    items needing attention, and password reuse warnings.

    Returns:
        Dict[str, Any]: Security health overview metrics and item flags.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, service_name, username_or_email, encrypted_password, updated_at FROM credentials WHERE user_id = ?",
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()

    total_credentials = len(rows)
    weak_count = 0
    moderate_count = 0
    strong_count = 0
    attention_items: List[Dict[str, Any]] = []

    seen_passwords: Dict[str, List[str]] = {}

    for row in rows:
        cred = dict(row)
        try:
            decrypted_pwd = decrypt_secret(cred["encrypted_password"], key)
            analysis = analyze_password(decrypted_pwd)
            strength = analysis["strength"]

            if strength == "Weak":
                weak_count += 1
                attention_items.append(
                    {
                        "id": cred["id"],
                        "service_name": cred["service_name"],
                        "issue": "Weak password strength",
                    }
                )
            elif strength == "Moderate":
                moderate_count += 1
            else:
                strong_count += 1

            if analysis["common"]:
                attention_items.append(
                    {
                        "id": cred["id"],
                        "service_name": cred["service_name"],
                        "issue": "Commonly used dictionary password",
                    }
                )

            # Track password reuse safely in memory
            seen_passwords.setdefault(decrypted_pwd, []).append(
                cred["service_name"]
            )

        except Exception:
            weak_count += 1

    # Detect reused passwords across services
    reused_services: Set[str] = set()
    for pwd, services in seen_passwords.items():
        if len(services) > 1:
            for s in services:
                reused_services.add(s)

    # Compute overall health score (0 - 100)
    health_score = 100
    if total_credentials > 0:
        health_score = int(
            ((strong_count * 1.0 + moderate_count * 0.6) / total_credentials)
            * 100
        )
        if len(reused_services) > 0:
            health_score = max(0, health_score - 20)

    return {
        "total_credentials": total_credentials,
        "weak_count": weak_count,
        "moderate_count": moderate_count,
        "strong_count": strong_count,
        "attention_count": len(attention_items),
        "attention_items": attention_items,
        "reused_services_count": len(reused_services),
        "health_score": health_score,
    }
