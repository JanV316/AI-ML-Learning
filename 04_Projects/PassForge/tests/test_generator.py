"""
Unit tests for passforge.generator module using Python unittest framework.
"""

import string
import unittest
from passforge.generator import MIN_PASSWORD_LENGTH, generate_password


class TestGenerator(unittest.TestCase):

    def test_correct_password_length(self):
        password = generate_password(16)
        self.assertEqual(len(password), 16)

    def test_minimum_valid_length(self):
        password = generate_password(MIN_PASSWORD_LENGTH)
        self.assertEqual(len(password), MIN_PASSWORD_LENGTH)

    def test_invalid_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            generate_password(7)

    def test_contains_uppercase(self):
        password = generate_password(12)
        self.assertTrue(any(c.isupper() for c in password))

    def test_contains_lowercase(self):
        password = generate_password(12)
        self.assertTrue(any(c.islower() for c in password))

    def test_contains_digit(self):
        password = generate_password(12)
        self.assertTrue(any(c.isdigit() for c in password))

    def test_contains_special_character(self):
        password = generate_password(12)
        self.assertTrue(any(c in string.punctuation for c in password))


if __name__ == "__main__":
    unittest.main()
