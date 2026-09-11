"""
Command Line Interface (CLI) module for PassForge V6.

Provides argparse CLI subcommand parsing, interactive menu fallback,
masked password entry using getpass, output formatting, and safe logging.
"""

import argparse
import getpass
import logging
import sys
from typing import Optional, Sequence

from passforge.analyzer import analyze_password, get_entropy_level
from passforge.generator import MIN_PASSWORD_LENGTH, generate_password
from passforge.security import PBKDF2_ITERATIONS, hash_password, verify_password

# Configure logging without writing sensitive password payload data
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.NullHandler()],
)
logger = logging.getLogger("PassForgeCLI")


def _safe_str(symbol: str, fallback: str) -> str:
    """Return unicode symbol if stdout supports it, else return safe ASCII fallback."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        symbol.encode(encoding)
        return symbol
    except UnicodeEncodeError:
        return fallback


def format_analysis_output(password: str) -> None:
    """Format and print password analysis results to standard output."""
    try:
        result = analyze_password(password)
    except ValueError as err:
        print(f"\nError: {err}\n", file=sys.stderr)
        return

    sym_check = _safe_str("✓", "[YES]")
    sym_cross = _safe_str("✗", "[NO]")
    sym_warn = _safe_str("⚠", "[WARN]")
    sym_bullet = _safe_str("•", "-")

    print("\n========== PASSWORD ANALYSIS ==========")
    print(f"\nLength           : {result['length']}")
    print(f"Uppercase        : {sym_check if result['uppercase'] else sym_cross}")
    print(f"Lowercase        : {sym_check if result['lowercase'] else sym_cross}")
    print(f"Numbers          : {sym_check if result['digit'] else sym_cross}")
    print(f"Special chars    : {sym_check if result['special'] else sym_cross}")
    print(f"Common password  : {sym_warn if result['common'] else sym_check}")
    print(f"Repeated chars   : {sym_warn if result['repeated'] else sym_check}")
    print(f"Sequential       : {sym_warn if result['sequential'] else sym_check}")
    print(f"Repeated pattern : {sym_warn if result['repeated_pattern'] else sym_check}")

    print(f"\nEntropy estimate : {result['entropy']:.2f} bits")
    print(f"Entropy level    : {get_entropy_level(result['entropy'])}")

    print(f"\nRule-based score : {result['score']}/7")
    print(f"Strength         : {result['strength']}")

    if result["warnings"]:
        print(f"\n{sym_warn} Security Warnings:")
        for warning in result["warnings"]:
            print(f"{sym_bullet} {warning}")

    if result["suggestions"]:
        print("\nSuggestions:")
        for suggestion in result["suggestions"]:
            print(f"{sym_bullet} {suggestion}")

    if not result["warnings"] and not result["suggestions"]:
        print(f"\n{sym_check} No obvious weaknesses detected.")

    print()


def handle_generate(
    length: Optional[int] = None, interactive: bool = False
) -> None:
    """Handle CLI password generation."""
    try:
        if length is None:
            user_input = input(
                f"\nEnter password length (minimum {MIN_PASSWORD_LENGTH}): "
            ).strip()
            length = int(user_input)

        password = generate_password(length)
        logger.info("Generated password of requested length %d", length)
        print("\nGenerated Password:")
        print(password)
        print()
    except ValueError as err:
        logger.warning("Password generation error: %s", err)
        print(f"\nError: {err}\n", file=sys.stderr)
        if not interactive:
            sys.exit(1)


def handle_analyze(
    password: Optional[str] = None, interactive: bool = False
) -> None:
    """Handle CLI password analysis using getpass for hidden typing."""
    try:
        if not password:
            password = getpass.getpass("Enter password to analyze: ")

        if not password:
            logger.warning("Empty password input for analysis")
            print("\nError: Password cannot be empty.\n", file=sys.stderr)
            if not interactive:
                sys.exit(1)
            return

        logger.info("Performing password analysis")
        format_analysis_output(password)
    except Exception as err:
        logger.warning("Password analysis error: %s", err)
        print(f"\nError: {err}\n", file=sys.stderr)
        if not interactive:
            sys.exit(1)


def handle_hash(
    password: Optional[str] = None, interactive: bool = False
) -> None:
    """Handle CLI password hashing using getpass."""
    try:
        if not password:
            password = getpass.getpass("Enter password to hash: ")

        if not password:
            logger.warning("Empty password input for hashing")
            print("\nError: Password cannot be empty.\n", file=sys.stderr)
            if not interactive:
                sys.exit(1)
            return

        salt, password_hash = hash_password(password)
        sym_warn = _safe_str("⚠", "[WARN]")
        logger.info("Generated password hash successfully")
        print("\n========== PASSWORD HASH ==========")
        print("\nAlgorithm  : PBKDF2-HMAC-SHA256")
        print(f"Iterations : {PBKDF2_ITERATIONS}")
        print(f"Salt       : {salt}")
        print(f"Hash       : {password_hash}")
        print(
            f"\n{sym_warn} Never store or share plaintext passwords in a real application.\n"
        )
    except ValueError as err:
        logger.warning("Password hashing error: %s", err)
        print(f"\nError: {err}\n", file=sys.stderr)
        if not interactive:
            sys.exit(1)


def handle_verify(
    password: Optional[str] = None,
    stored_salt: Optional[str] = None,
    stored_hash: Optional[str] = None,
    interactive: bool = False,
) -> None:
    """Handle CLI password verification using getpass."""
    try:
        if not password:
            password = getpass.getpass("Enter password: ")

        if not password:
            logger.warning("Empty password input for verification")
            print("\nError: Password cannot be empty.\n", file=sys.stderr)
            if not interactive:
                sys.exit(1)
            return

        if stored_salt is None:
            stored_salt = input("Enter stored salt: ").strip()

        if stored_hash is None:
            stored_hash = input("Enter stored hash: ").strip()

        is_valid = verify_password(password, stored_salt, stored_hash)
        sym_check = _safe_str("✓", "[PASS]")
        sym_cross = _safe_str("✗", "[FAIL]")
        logger.info("Password verification process completed")
        if is_valid:
            print(f"\n{sym_check} Password verification successful.")
        else:
            print(f"\n{sym_cross} Password verification failed.")
            if not interactive:
                sys.exit(1)
        print()
    except ValueError as err:
        logger.warning("Password verification error: %s", err)
        print(f"\nError: {err}\n", file=sys.stderr)
        if not interactive:
            sys.exit(1)


def run_interactive_menu() -> None:
    """Main interactive terminal menu interface for PassForge V6."""
    while True:
        print("========================================")
        print("              PASSFORGE")
        print("       Password Security Toolkit")
        print("========================================")
        print()
        print("1. Generate Password")
        print("2. Analyze Password")
        print("3. Hash Password")
        print("4. Verify Password")
        print("5. Launch Web Interface")
        print("6. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            handle_generate(interactive=True)
        elif choice == "2":
            handle_analyze(interactive=True)
        elif choice == "3":
            handle_hash(interactive=True)
        elif choice == "4":
            handle_verify(interactive=True)
        elif choice == "5":
            from passforge.web import run_web
            run_web()
            break
        elif choice == "6":
            logger.info("Exiting application menu")
            print("\nThank you for using PassForge!")
            break
        else:
            logger.warning("Invalid menu option selected: %s", choice)
            print("\nInvalid option. Please choose 1-6.\n")


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argparse CLI command parser."""
    parser = argparse.ArgumentParser(
        prog="passforge",
        description="PassForge - Password Security Toolkit (CLI & Web)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Launch Flask web interface",
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available subcommands"
    )

    # Subcommand: generate
    gen_parser = subparsers.add_parser(
        "generate",
        help="Generate a cryptographically secure random password",
    )
    gen_parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=12,
        help="Password length (minimum 8, default 12)",
    )

    # Subcommand: analyze
    subparsers.add_parser(
        "analyze",
        help="Analyze password strength, entropy, and weak patterns",
    )

    # Subcommand: hash
    subparsers.add_parser(
        "hash",
        help="Hash a password securely using PBKDF2-HMAC-SHA256",
    )

    # Subcommand: verify
    subparsers.add_parser(
        "verify",
        help="Verify a candidate password against a stored salt and hash",
    )

    # Subcommand: web
    web_parser = subparsers.add_parser(
        "web",
        help="Launch Flask web application interface",
    )
    web_parser.add_argument(
        "--port", type=int, default=5000, help="Port to run web server on"
    )
    web_parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host address"
    )

    # Subcommand: menu
    subparsers.add_parser(
        "menu",
        help="Launch the interactive terminal menu",
    )

    return parser


def main(argv: Optional[Sequence[str]] = None) -> None:
    """Main CLI entry point for PassForge V6."""
    parser = build_parser()

    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        run_interactive_menu()
        return

    parsed_args = parser.parse_args(argv)

    if parsed_args.web or parsed_args.command == "web":
        from passforge.web import run_web
        port = getattr(parsed_args, "port", 5000)
        host = getattr(parsed_args, "host", "127.0.0.1")
        run_web(host=host, port=port)
    elif parsed_args.command == "generate":
        handle_generate(length=parsed_args.length)
    elif parsed_args.command == "analyze":
        handle_analyze()
    elif parsed_args.command == "hash":
        handle_hash()
    elif parsed_args.command == "verify":
        handle_verify()
    elif parsed_args.command == "menu":
        run_interactive_menu()
    else:
        parser.print_help()
