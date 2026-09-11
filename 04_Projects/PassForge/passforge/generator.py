"""
Secure password generator module for PassForge.

Provides cryptographically secure password generation and passphrase creation
using Python's `secrets` module.
"""

import secrets
import string
from typing import List

MIN_PASSWORD_LENGTH: int = 8

# Concise EFF-inspired wordlist for passphrase generation
PASSPHRASE_WORDLIST: List[str] = [
    "correct", "horse", "battery", "staple", "shadow", "falcon", "orbit", "prism",
    "vertex", "magnet", "nebula", "quantum", "beacon", "timber", "canyon", "velvet",
    "cobalt", "anchor", "summit", "harbor", "cipher", "granite", "aurora", "breeze",
    "glacier", "zenith", "pyramid", "compass", "voyage", "solace", "horizon", "thistle",
    "whisper", "echo", "cascade", "mariner", "radiance", "solitude", "catalyst", "symphony",
]


def generate_password(
    length: int = 12,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length (int): Desired length of the password (minimum 8). Defaults to 12.
        use_uppercase (bool): Include uppercase characters. Defaults to True.
        use_lowercase (bool): Include lowercase characters. Defaults to True.
        use_digits (bool): Include numeric digits. Defaults to True.
        use_symbols (bool): Include special symbols. Defaults to True.

    Returns:
        str: Cryptographically secure generated password.

    Raises:
        ValueError: If length is less than MIN_PASSWORD_LENGTH (8) or if no character set is selected.
    """
    if length < MIN_PASSWORD_LENGTH:
        raise ValueError(
            f"Password length must be at least {MIN_PASSWORD_LENGTH} characters."
        )

    pools = []
    required_chars = []

    if use_uppercase:
        pools.append(string.ascii_uppercase)
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        pools.append(string.ascii_lowercase)
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        pools.append(string.digits)
        required_chars.append(secrets.choice(string.digits))
    if use_symbols:
        pools.append(string.punctuation)
        required_chars.append(secrets.choice(string.punctuation))

    if not pools:
        raise ValueError("At least one character type must be selected.")

    all_characters = "".join(pools)
    password_characters = list(required_chars)

    # Fill remaining length requirement
    remaining_length = length - len(password_characters)
    for _ in range(remaining_length):
        password_characters.append(secrets.choice(all_characters))

    # Secure shuffle using SystemRandom
    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)


def generate_passphrase(num_words: int = 4, separator: str = "-") -> str:
    """
    Generate a cryptographically secure multi-word passphrase.

    Args:
        num_words (int): Number of words (minimum 3). Defaults to 4.
        separator (str): Character separating words. Defaults to '-'.

    Returns:
        str: Cryptographically secure passphrase.

    Raises:
        ValueError: If num_words is less than 3.
    """
    if num_words < 3:
        raise ValueError("Passphrase must contain at least 3 words.")

    words = [secrets.choice(PASSPHRASE_WORDLIST) for _ in range(num_words)]
    return separator.join(words)
