"""
Unit tests for vault encryption, decryption, CRUD operations, and health analysis in PassForge V7.
"""

import os
import tempfile
import unittest

from passforge.auth import register_user
from passforge.models import get_user_by_username_or_email, init_db
from passforge.vault import (
    add_credential,
    analyze_user_vault,
    decrypt_secret,
    delete_credential,
    derive_vault_key,
    encrypt_secret,
    get_credential_by_id,
    get_user_credentials,
    update_credential,
)


class TestVault(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        init_db(self.db_path)
        register_user("alice", "alice@example.com", "MasterPwd123!", db_path=self.db_path)
        self.user = get_user_by_username_or_email("alice", db_path=self.db_path)
        self.vault_key = derive_vault_key("MasterPwd123!", self.user["password_salt"])

    def tearDown(self):
        os.close(self.db_fd)
        os.remove(self.db_path)

    def test_fernet_encryption_decryption(self):
        plaintext = "MySecretVaultPassword!"
        ciphertext = encrypt_secret(plaintext, self.vault_key)
        self.assertNotEqual(plaintext, ciphertext)

        decrypted = decrypt_secret(ciphertext, self.vault_key)
        self.assertEqual(plaintext, decrypted)

    def test_add_and_retrieve_credential(self):
        cred_id = add_credential(
            user_id=self.user["id"],
            service_name="GitHub",
            username_or_email="alice_git",
            plaintext_password="GitSecretPassword123!",
            key=self.vault_key,
            url="https://github.com",
            db_path=self.db_path,
        )
        self.assertGreater(cred_id, 0)

        creds = get_user_credentials(self.user["id"], db_path=self.db_path)
        self.assertEqual(len(creds), 1)
        self.assertEqual(creds[0]["service_name"], "GitHub")
        self.assertEqual(creds[0]["masked_password"], "••••••••••••")

    def test_update_credential(self):
        cred_id = add_credential(
            user_id=self.user["id"],
            service_name="GitHub",
            username_or_email="alice_git",
            plaintext_password="OldPassword123!",
            key=self.vault_key,
            db_path=self.db_path,
        )
        success = update_credential(
            cred_id=cred_id,
            user_id=self.user["id"],
            service_name="GitHub Enterprise",
            username_or_email="alice_git_ent",
            plaintext_password="NewPassword456!",
            key=self.vault_key,
            db_path=self.db_path,
        )
        self.assertTrue(success)

        updated = get_credential_by_id(cred_id, self.user["id"], db_path=self.db_path)
        self.assertEqual(updated["service_name"], "GitHub Enterprise")
        decrypted = decrypt_secret(updated["encrypted_password"], self.vault_key)
        self.assertEqual(decrypted, "NewPassword456!")

    def test_delete_credential(self):
        cred_id = add_credential(
            user_id=self.user["id"],
            service_name="GitHub",
            username_or_email="alice_git",
            plaintext_password="Password123!",
            key=self.vault_key,
            db_path=self.db_path,
        )
        success = delete_credential(cred_id, self.user["id"], db_path=self.db_path)
        self.assertTrue(success)

        creds = get_user_credentials(self.user["id"], db_path=self.db_path)
        self.assertEqual(len(creds), 0)

    def test_vault_health_analysis(self):
        add_credential(
            user_id=self.user["id"],
            service_name="Service 1",
            username_or_email="alice",
            plaintext_password="123456",  # Weak common password
            key=self.vault_key,
            db_path=self.db_path,
        )
        add_credential(
            user_id=self.user["id"],
            service_name="Service 2",
            username_or_email="alice",
            plaintext_password="K#9xP$m2L!vQ8zW9",  # Strong password
            key=self.vault_key,
            db_path=self.db_path,
        )

        health = analyze_user_vault(self.user["id"], self.vault_key, db_path=self.db_path)
        self.assertEqual(health["total_credentials"], 2)
        self.assertEqual(health["weak_count"], 1)
        self.assertEqual(health["strong_count"], 1)
        self.assertGreater(health["attention_count"], 0)


if __name__ == "__main__":
    unittest.main()
