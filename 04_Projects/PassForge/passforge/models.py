"""
Database models and SQLite connection management for PassForge V7.

Provides data persistence for users, encrypted credentials, and security audit events.
"""

import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# Determine path for SQLite database file in project instance directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "passforge.db")


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Establish and return a connection to the SQLite database.

    Args:
        db_path (Optional[str]): Database file path. Defaults to DB_PATH.

    Returns:
        sqlite3.Connection: Configured connection with Row factory.
    """
    target_path = db_path or DB_PATH
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Initialize database tables if they do not exist."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Table: users
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'USER',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        )
        """
    )

    # Table: credentials
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service_name TEXT NOT NULL,
            username_or_email TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            url TEXT,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    # Table: audit_events
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT NOT NULL,
            event_type TEXT NOT NULL,
            ip_address TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
        """
    )

    conn.commit()
    conn.close()


def create_user(
    username: str,
    email: str,
    password_salt: str,
    password_hash: str,
    role: str = "USER",
    db_path: Optional[str] = None,
) -> int:
    """Create a new user record."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    created_at = datetime.utcnow().isoformat()

    cursor.execute(
        """
        INSERT INTO users (username, email, password_salt, password_hash, role, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, 1, ?)
        """,
        (username, email, password_salt, password_hash, role, created_at),
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_user_by_username_or_email(
    identifier: str, db_path: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Retrieve user record by username or email."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)",
        (identifier, identifier),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(
    user_id: int, db_path: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Retrieve user record by ID."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_users(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve all users for admin overview."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, role, is_active, created_at FROM users ORDER BY id ASC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_count(db_path: Optional[str] = None) -> Tuple[int, int]:
    """Return total users count and active users count."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(is_active) FROM users")
    total, active = cursor.fetchone()
    conn.close()
    return total or 0, active or 0


def set_user_active_status(
    user_id: int, is_active: bool, db_path: Optional[str] = None
) -> None:
    """Toggle or set user active status."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET is_active = ? WHERE id = ?",
        (1 if is_active else 0, user_id),
    )
    conn.commit()
    conn.close()


def log_audit_event(
    user_id: Optional[int],
    username: str,
    event_type: str,
    ip_address: Optional[str] = None,
    db_path: Optional[str] = None,
) -> None:
    """Log a security audit event without sensitive payload information."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    cursor.execute(
        """
        INSERT INTO audit_events (user_id, username, event_type, ip_address, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, username, event_type, ip_address, created_at),
    )
    conn.commit()
    conn.close()


def get_audit_events(
    limit: int = 100, db_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve recent security audit log entries."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM audit_events ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
