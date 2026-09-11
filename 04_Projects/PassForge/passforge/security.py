"""
Security module for PassForge V5.

Provides password hashing using PBKDF2-HMAC-SHA256 and constant-time verification.

SECURITY NOTE:
This module is intended for educational demonstration purposes.
Production applications should evaluate modern password hashing algorithms
such as Argon2id (or bcrypt) according to their security requirements.
"""

import base64
import hashlib
import hmac
import secrets
from typing import Tuple

PBKDF2_ITERATIONS: int = 600_000
SALT_LENGTH: int = 16


def hash_password(
    password: str, iterations: int = PBKDF2_ITERATIONS
) -> Tuple[str, str]:
    """
    Hash a password using PBKDF2-HMAC-SHA256 with a randomly generated salt.

    Args:
        password (str): Plaintext candidate password. Must not be empty.
        iterations (int): PBKDF2 iteration count. Defaults to 600,000.

    Returns:
        Tuple[str, str]: Base64-encoded salt string and Base64-encoded hash string.

    Raises:
        ValueError: If password is empty.
    """
    if not password:
        raise ValueError("Password cannot be empty.")

    salt = secrets.token_bytes(SALT_LENGTH)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )

    encoded_salt = base64.b64encode(salt).decode("utf-8")
    encoded_hash = base64.b64encode(password_hash).decode("utf-8")

    return encoded_salt, encoded_hash


def verify_password(
    password: str,
    stored_salt: str,
    stored_hash: str,
    iterations: int = PBKDF2_ITERATIONS,
) -> bool:
    """
    Verify a candidate password against a stored salt and hash using constant-time comparison.

    Args:
        password (str): Candidate plaintext password. Must not be empty.
        stored_salt (str): Base64-encoded salt string.
        stored_hash (str): Base64-encoded expected hash string.
        iterations (int): PBKDF2 iteration count used during hashing.

    Returns:
        bool: True if verification succeeds, False otherwise.

    Raises:
        ValueError: If password is empty.
    """
    if not password:
        raise ValueError("Password cannot be empty.")

    if not stored_salt or not stored_hash:
        return False

    try:
        salt = base64.b64decode(stored_salt)
        expected_hash = base64.b64decode(stored_hash)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, iterations
        )

        return hmac.compare_digest(password_hash, expected_hash)

    except (ValueError, TypeError, Exception):
        return False
