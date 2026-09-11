"""
Unit tests for passforge.web module (Flask Web Application) using unittest framework.
"""

import unittest
from passforge.security import hash_password
from passforge.web import app


class TestWeb(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"PassForge", response.data)
        self.assertIn(b"Password Security Toolkit", response.data)

    def test_generate_page_get(self):
        response = self.client.get("/generate")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Secure Password & Passphrase Generator", response.data)

    def test_analyze_page_get(self):
        response = self.client.get("/analyze")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password Analyzer", response.data)

    def test_hash_page_get(self):
        response = self.client.get("/hash")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password Hashing", response.data)

    def test_verify_page_get(self):
        response = self.client.get("/verify")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password Verification", response.data)

    def test_valid_password_generation_post(self):
        response = self.client.post("/generate", data={"length": "16"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Generated Output", response.data)

    def test_invalid_password_length_post(self):
        response = self.client.post("/generate", data={"length": "4"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password length must be at least 8 characters", response.data)

    def test_password_analysis_post(self):
        response = self.client.post("/analyze", data={"password": "SecureP@ssw0rd123!"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Analysis Results", response.data)
        self.assertIn(b"Theoretical Entropy", response.data)

    def test_password_hashing_post(self):
        response = self.client.post("/hash", data={"password": "SecureP@ssw0rd123!"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cryptographic Hash Output", response.data)
        self.assertIn(b"PBKDF2-HMAC-SHA256", response.data)

    def test_correct_password_verification_post(self):
        password = "MySecurePassword123!"
        salt, pwd_hash = hash_password(password)
        
        response = self.client.post(
            "/verify",
            data={
                "password": password,
                "salt": salt,
                "hash": pwd_hash,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password verification successful", response.data)

    def test_incorrect_password_verification_post(self):
        password = "MySecurePassword123!"
        salt, pwd_hash = hash_password(password)
        
        response = self.client.post(
            "/verify",
            data={
                "password": "WrongPassword123!",
                "salt": salt,
                "hash": pwd_hash,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password verification failed", response.data)


if __name__ == "__main__":
    unittest.main()
