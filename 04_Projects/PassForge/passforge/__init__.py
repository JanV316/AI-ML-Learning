"""
PassForge - Password Security Toolkit (V6).

A modular Python toolkit for generating, analyzing, hashing, and verifying passwords.
"""

__version__ = "6.0.0"

from .analyzer import (
    analyze_password,
    estimate_entropy,
    get_entropy_level,
    has_repeated_characters,
    has_repeated_pattern,
    has_sequential_characters,
    is_common_password,
)
from .generator import MIN_PASSWORD_LENGTH, generate_password
from .security import PBKDF2_ITERATIONS, hash_password, verify_password

__all__ = [
    "generate_password",
    "MIN_PASSWORD_LENGTH",
    "analyze_password",
    "estimate_entropy",
    "get_entropy_level",
    "is_common_password",
    "has_repeated_characters",
    "has_sequential_characters",
    "has_repeated_pattern",
    "hash_password",
    "verify_password",
    "PBKDF2_ITERATIONS",
]
