"""
Unit tests for passforge.cli module using Python unittest framework.
"""

from io import StringIO
import unittest
from unittest.mock import patch

from passforge.cli import build_parser, main
from passforge.security import hash_password


class TestCLI(unittest.TestCase):

    def test_parser_generation_args(self):
        parser = build_parser()
        args = parser.parse_args(["generate", "--length", "20"])
        self.assertEqual(args.command, "generate")
        self.assertEqual(args.length, 20)

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_generate_command(self, mock_stdout):
        main(["generate", "--length", "16"])
        output = mock_stdout.getvalue()
        self.assertIn("Generated Password:", output)

    @patch("getpass.getpass", return_value="SecureP@ssw0rd123!")
    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_analyze_command(self, mock_stdout, mock_getpass):
        main(["analyze"])
        output = mock_stdout.getvalue()
        self.assertIn("PASSWORD ANALYSIS", output)
        self.assertIn("Entropy estimate", output)

    @patch("getpass.getpass", return_value="SecureP@ssw0rd123!")
    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_hash_command(self, mock_stdout, mock_getpass):
        main(["hash"])
        output = mock_stdout.getvalue()
        self.assertIn("PASSWORD HASH", output)
        self.assertIn("PBKDF2-HMAC-SHA256", output)

    @patch("getpass.getpass", return_value="SecureP@ssw0rd123!")
    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_verify_command_success(self, mock_stdout, mock_getpass):
        salt, pwd_hash = hash_password("SecureP@ssw0rd123!")
        with patch("builtins.input", side_effect=[salt, pwd_hash]):
            main(["verify"])
            output = mock_stdout.getvalue()
            self.assertIn("Password verification successful", output)

    @patch("getpass.getpass", return_value="WrongPassword123!")
    @patch("sys.stderr", new_callable=StringIO)
    def test_cli_verify_command_failure(self, mock_stderr, mock_getpass):
        salt, pwd_hash = hash_password("SecureP@ssw0rd123!")
        with patch("builtins.input", side_effect=[salt, pwd_hash]):
            with self.assertRaises(SystemExit) as cm:
                main(["verify"])
            self.assertEqual(cm.exception.code, 1)

    @patch("sys.stderr", new_callable=StringIO)
    def test_cli_generate_invalid_length(self, mock_stderr):
        with self.assertRaises(SystemExit) as cm:
            main(["generate", "--length", "5"])
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error:", mock_stderr.getvalue())

    @patch("getpass.getpass", return_value="")
    @patch("sys.stderr", new_callable=StringIO)
    def test_cli_analyze_empty_password(self, mock_stderr, mock_getpass):
        with self.assertRaises(SystemExit) as cm:
            main(["analyze"])
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Password cannot be empty", mock_stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
