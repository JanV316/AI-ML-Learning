"""
Password analyzer module for PassForge V5.

Evaluates password length, character diversity, common weak patterns,
and estimates theoretical entropy using rule-based heuristics.
"""

import math
import string
from typing import Any, Dict, List

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "123456789",
    "1234567890",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "letmein",
    "welcome",
    "abc123",
    "iloveyou",
    "monkey",
    "dragon",
    "football",
    "login",
    "passw0rd",
}


def is_common_password(password: str) -> bool:
    """
    Check whether a password is present in the common passwords list.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if password is common, False otherwise.

    Raises:
        ValueError: If password is empty.
    """
    if not password:
        raise ValueError("Password cannot be empty.")
    return password.lower() in COMMON_PASSWORDS


def has_repeated_characters(password: str) -> bool:
    """
    Detect three or more identical consecutive characters.

    Args:
        password (str): The password to analyze.

    Returns:
        bool: True if three consecutive identical characters are found.

    Raises:
        ValueError: If password is empty.
    """
    if not password:
        raise ValueError("Password cannot be empty.")
    if len(password) < 3:
        return False

    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            return True

    return False


def has_sequential_characters(password: str) -> bool:
    """
    Detect simple ascending or descending sequential patterns (e.g., 'abc', 'cba', '123', '321').

    Args:
        password (str): The password to analyze.

    Returns:
        bool: True if sequential pattern is detected.

    Raises:
        ValueError: If password is empty.
    """
    if not password:
        raise ValueError("Password cannot be empty.")

    pwd_lower = password.lower()
    sequences = [string.ascii_lowercase, string.digits]

    for sequence in sequences:
        for i in range(len(sequence) - 2):
            pattern = sequence[i : i + 3]
            if pattern in pwd_lower or pattern[::-1] in pwd_lower:
                return True

    return False


def has_repeated_pattern(password: str) -> bool:
    """
    Detect repeated substring patterns such as 'abcabc' or '123123'.

    Args:
        password (str): The password to analyze.

    Returns:
        bool: True if a repeating pattern fills the entire password.

    Raises:
        ValueError: If password is empty.
    """
    if not password:
        raise ValueError("Password cannot be empty.")

    length = len(password)
    for pattern_length in range(1, length // 2 + 1):
        if length % pattern_length != 0:
            continue

        pattern = password[:pattern_length]
        if pattern * (length // pattern_length) == password:
            return True

    return False


def estimate_entropy(password: str) -> float:
    """
    Estimate theoretical entropy in bits based on character pool size.

    Args:
        password (str): The password to analyze.

    Returns:
        float: Calculated entropy in bits.

    Raises:
        ValueError: If password is empty.
    """
    if not password:
        raise ValueError("Password cannot be empty.")

    pool_size = 0
    if any(char.islower() for char in password):
        pool_size += 26
    if any(char.isupper() for char in password):
        pool_size += 26
    if any(char.isdigit() for char in password):
        pool_size += 10
    if any(char in string.punctuation for char in password):
        pool_size += len(string.punctuation)

    if pool_size == 0:
        return 0.0

    return len(password) * math.log2(pool_size)


def get_entropy_level(entropy: float) -> str:
    """
    Classify calculated entropy into descriptive security levels.

    Args:
        entropy (float): Theoretical entropy in bits.

    Returns:
        str: Classification level ('Very Low', 'Low', 'Moderate', 'High', 'Very High').
    """
    if entropy < 40:
        return "Very Low"
    elif entropy < 60:
        return "Low"
    elif entropy < 80:
        return "Moderate"
    elif entropy < 100:
        return "High"
    else:
        return "Very High"


def analyze_password(password: str) -> Dict[str, Any]:
    """
    Perform complete rule-based analysis and entropy evaluation on a password.

    Args:
        password (str): The password to analyze.

    Returns:
        Dict[str, Any]: Structured dictionary containing metrics, flags, score, strength, warnings, and suggestions.

    Raises:
        ValueError: If password is empty.
    """
    if not password:
        raise ValueError("Password cannot be empty.")

    length = len(password)
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)

    common = is_common_password(password)
    repeated = has_repeated_characters(password)
    sequential = has_sequential_characters(password)
    repeated_pattern = has_repeated_pattern(password)
    entropy = estimate_entropy(password)

    score = 0
    suggestions: List[str] = []
    warnings: List[str] = []

    # Length criteria
    if length >= 12:
        score += 2
    else:
        suggestions.append("Use at least 12 characters.")

    if length >= 16:
        score += 1

    # Character diversity criteria
    if has_uppercase:
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if has_lowercase:
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if has_digit:
        score += 1
    else:
        suggestions.append("Add numbers.")

    if has_special:
        score += 1
    else:
        suggestions.append("Add special characters.")

    # Pattern penalties
    if common:
        score -= 3
        warnings.append("This is a commonly used password.")

    if repeated:
        score -= 2
        warnings.append("Repeated characters detected.")

    if sequential:
        score -= 2
        warnings.append("Sequential characters detected.")

    if repeated_pattern:
        score -= 2
        warnings.append("Repeated pattern detected.")

    score = max(score, 0)

    # Determine strength category
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    elif score <= 6:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        "length": length,
        "uppercase": has_uppercase,
        "lowercase": has_lowercase,
        "digit": has_digit,
        "special": has_special,
        "common": common,
        "repeated": repeated,
        "sequential": sequential,
        "repeated_pattern": repeated_pattern,
        "entropy": entropy,
        "strength": strength,
        "score": score,
        "warnings": warnings,
        "suggestions": suggestions,
    }
