"""
Authentication and Authorization module for PassForge V7.

Handles registration, credential verification, session management, role-based access control,
and security audit logging.
"""

from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple
from flask import flash, redirect, request, session, url_for

from passforge.models import (
    create_user,
    get_user_by_id,
    get_user_by_username_or_email,
    get_user_count,
    log_audit_event,
)
from passforge.security import hash_password, verify_password
from passforge.vault import derive_vault_key


def register_user(
    username: str,
    email: str,
    password: str,
    ip_address: Optional[str] = None,
    db_path: Optional[str] = None,
) -> Tuple[bool, str]:
    """
    Register a new user account.

    The first registered user is automatically assigned the ADMIN role.
    Subsequent users receive the USER role.

    Args:
        username (str): Target username.
        email (str): Target email address.
        password (str): Plaintext authentication password.
        ip_address (Optional[str]): Client IP address for audit logging.
        db_path (Optional[str]): Database path for testing.

    Returns:
        Tuple[bool, str]: Success status and message string.
    """
    username = username.strip()
    email = email.strip()

    if not username or not email or not password:
        return False, "All fields are required."

    if len(username) < 3:
        return False, "Username must be at least 3 characters long."

    if "@" not in email:
        return False, "Please enter a valid email address."

    if len(password) < 8:
        return False, "Authentication password must be at least 8 characters long."

    existing = get_user_by_username_or_email(username, db_path)
    if existing:
        return False, "Username or email is already registered."

    existing_email = get_user_by_username_or_email(email, db_path)
    if existing_email:
        return False, "Username or email is already registered."

    # Determine role: First user is ADMIN
    total_users, _ = get_user_count(db_path)
    role = "ADMIN" if total_users == 0 else "USER"

    salt, pwd_hash = hash_password(password)
    user_id = create_user(
        username=username,
        email=email,
        password_salt=salt,
        password_hash=pwd_hash,
        role=role,
        db_path=db_path,
    )

    log_audit_event(
        user_id=user_id,
        username=username,
        event_type="USER_REGISTERED",
        ip_address=ip_address,
        db_path=db_path,
    )

    return True, "Account registered successfully. Please log in."


def authenticate_user(
    identifier: str,
    password: str,
    ip_address: Optional[str] = None,
    db_path: Optional[str] = None,
) -> Tuple[bool, str, Optional[Dict[str, Any]], Optional[bytes]]:
    """
    Authenticate a user by username/email and password.

    Args:
        identifier (str): Username or email.
        password (str): Plaintext candidate password.
        ip_address (Optional[str]): Client IP for audit logging.
        db_path (Optional[str]): Database path for testing.

    Returns:
        Tuple[bool, str, Optional[Dict], Optional[bytes]]: (success, message, user_dict, vault_key)
    """
    identifier = identifier.strip()

    if not identifier or not password:
        return False, "Invalid username or password.", None, None

    user = get_user_by_username_or_email(identifier, db_path)
    if not user:
        log_audit_event(
            user_id=None,
            username=identifier,
            event_type="LOGIN_FAILED",
            ip_address=ip_address,
            db_path=db_path,
        )
        return False, "Invalid username or password.", None, None

    if not user["is_active"]:
        log_audit_event(
            user_id=user["id"],
            username=user["username"],
            event_type="LOGIN_BLOCKED_DEACTIVATED",
            ip_address=ip_address,
            db_path=db_path,
        )
        return (
            False,
            "Account is deactivated. Please contact an administrator.",
            None,
            None,
        )

    is_valid = verify_password(
        password=password,
        stored_salt=user["password_salt"],
        stored_hash=user["password_hash"],
    )

    if not is_valid:
        log_audit_event(
            user_id=user["id"],
            username=user["username"],
            event_type="LOGIN_FAILED",
            ip_address=ip_address,
            db_path=db_path,
        )
        return False, "Invalid username or password.", None, None

    # Derive vault key for active session
    vault_key = derive_vault_key(password, user["password_salt"])

    log_audit_event(
        user_id=user["id"],
        username=user["username"],
        event_type="LOGIN_SUCCESS",
        ip_address=ip_address,
        db_path=db_path,
    )

    return True, "Login successful.", user, vault_key


def login_required(f: Callable) -> Callable:
    """Decorator to enforce user login for protected routes."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f: Callable) -> Callable:
    """Decorator to enforce ADMIN role for privileged admin routes."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))

        if session.get("role") != "ADMIN":
            flash(
                "Access denied. Administrator privileges required.", "danger"
            )
            return redirect(url_for("dashboard"))

        return f(*args, **kwargs)

    return decorated_function
