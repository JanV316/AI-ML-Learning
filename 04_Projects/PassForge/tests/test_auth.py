"""
Unit tests for authentication, user registration, sessions, and roles in PassForge V7.
"""

import os
import tempfile
import unittest

from passforge.auth import authenticate_user, register_user
from passforge.models import get_all_users, get_user_by_username_or_email, init_db, set_user_active_status


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        init_db(self.db_path)

    def tearDown(self):
        os.close(self.db_fd)
        os.remove(self.db_path)

    def test_registration_success(self):
        success, msg = register_user(
            "alice", "alice@example.com", "Password123!", db_path=self.db_path
        )
        self.assertTrue(success)
        user = get_user_by_username_or_email("alice", db_path=self.db_path)
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "alice")
        self.assertEqual(user["role"], "ADMIN")  # First user is ADMIN

    def test_second_registration_gets_user_role(self):
        register_user("alice", "alice@example.com", "Password123!", db_path=self.db_path)
        register_user("bob", "bob@example.com", "Password123!", db_path=self.db_path)

        bob = get_user_by_username_or_email("bob", db_path=self.db_path)
        self.assertEqual(bob["role"], "USER")

    def test_duplicate_registration_fails(self):
        register_user("alice", "alice@example.com", "Password123!", db_path=self.db_path)
        success, msg = register_user(
            "alice", "alice2@example.com", "Password123!", db_path=self.db_path
        )
        self.assertFalse(success)
        self.assertIn("already registered", msg)

    def test_authenticate_success(self):
        register_user("alice", "alice@example.com", "Password123!", db_path=self.db_path)
        success, msg, user, key = authenticate_user(
            "alice", "Password123!", db_path=self.db_path
        )
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertIsNotNone(key)

    def test_authenticate_invalid_password(self):
        register_user("alice", "alice@example.com", "Password123!", db_path=self.db_path)
        success, msg, user, key = authenticate_user(
            "alice", "WrongPassword123!", db_path=self.db_path
        )
        self.assertFalse(success)
        self.assertIsNone(user)
        self.assertIsNone(key)

    def test_deactivated_user_login_blocked(self):
        register_user("alice", "alice@example.com", "Password123!", db_path=self.db_path)
        user = get_user_by_username_or_email("alice", db_path=self.db_path)
        set_user_active_status(user["id"], False, db_path=self.db_path)

        success, msg, user, key = authenticate_user(
            "alice", "Password123!", db_path=self.db_path
        )
        self.assertFalse(success)
        self.assertIn("deactivated", msg)


if __name__ == "__main__":
    unittest.main()
