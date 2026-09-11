"""
Unit tests for passforge.security module using Python unittest framework.
"""

import unittest
from passforge.security import hash_password, verify_password


class TestSecurity(unittest.TestCase):

    def test_hash_generation(self):
        salt, pwd_hash = hash_password("MySecretPassword123!", iterations=1000)
        self.assertIsInstance(salt, str)
        self.assertIsInstance(pwd_hash, str)
        self.assertGreater(len(salt), 0)
        self.assertGreater(len(pwd_hash), 0)

    def test_correct_password_verification(self):
        password = "MySecurePassword123!"
        salt, pwd_hash = hash_password(password, iterations=1000)
        self.assertTrue(
            verify_password(password, salt, pwd_hash, iterations=1000)
        )

    def test_incorrect_password_verification(self):
        password = "MySecurePassword123!"
        salt, pwd_hash = hash_password(password, iterations=1000)
        self.assertFalse(
            verify_password("WrongPassword!", salt, pwd_hash, iterations=1000)
        )

    def test_same_password_produces_different_salts(self):
        password = "IdenticalPassword123!"
        salt1, hash1 = hash_password(password, iterations=1000)
        salt2, hash2 = hash_password(password, iterations=1000)
        self.assertNotEqual(salt1, salt2)
        self.assertNotEqual(hash1, hash2)

    def test_empty_password_handling(self):
        with self.assertRaises(ValueError):
            hash_password("")

        with self.assertRaises(ValueError):
            verify_password("", "some_salt", "some_hash")

    def test_invalid_salt_hash_handling(self):
        self.assertFalse(
            verify_password("password", "invalid_salt", "invalid_hash")
        )
        self.assertFalse(verify_password("password", "", ""))


if __name__ == "__main__":
    unittest.main()
