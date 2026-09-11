# PassForge Security Policy & Architecture Model

PassForge is a privacy-focused password security toolkit and personal credential vault designed for educational and portfolio demonstration.

---

## 🏛️ 1. Security Architecture Overview

PassForge enforces strict separation of concerns across core security modules:

- **`passforge/security.py`**: Handles one-way authentication key derivation and constant-time string comparison.
- **`passforge/vault.py`**: Manages two-way symmetric encryption/decryption for saved vault secrets.
- **`passforge/auth.py`**: Enforces user authentication, session security, and role-based authorization.
- **`passforge/models.py`**: Manages SQLite data storage for users, encrypted credentials, and security audit logs.

---

## 🔒 2. Authentication Password Handling

User authentication passwords are **never stored as plaintext**.

1. When a user registers or updates their authentication password:
   - A 16-byte cryptographically secure random salt is generated via Python's `secrets.token_bytes()`.
   - The password is derived using `PBKDF2-HMAC-SHA256` with **600,000 iterations**.
   - The Base64 salt and hash are stored in the `users` table.
2. During login:
   - The candidate password is derived using the stored salt and compared in **constant time** via `hmac.compare_digest()`.
3. Account enumeration prevention:
   - Failed authentication attempts return generic error messages ("Invalid username or password.").

---

## 🛡️ 3. Vault Credential Encryption

Vault credentials must be retrieved by their authorized owner, so they are **encrypted symmetrically** rather than hashed.

- **Key Derivation**: When a user logs in, a 32-byte `Fernet` key (`AES-128-CBC` + `HMAC-SHA256`) is derived from the user's plaintext password and salt using `PBKDF2HMAC`.
- **In-Memory Lifetime**: The derived vault encryption key exists only in active server session memory and is destroyed upon logout or session termination.
- **Data at Rest**: Vault secrets stored in `credentials.encrypted_password` are encrypted ciphertext strings.
- **Zero-Knowledge Admin Policy**: Administrators can manage user accounts and inspect audit metadata, but **cannot decrypt user vault secrets** because decryption requires the user's authentication password, which is never stored on disk.

---

## 🔑 4. Session Security & Authorization

- **Session Cookies**: Formatted with `HttpOnly=True` and `SameSite=Lax` to mitigate Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) vectors.
- **User Isolation**: Database queries for vault CRUD operations explicitly restrict lookups using `user_id = session['user_id']`. User A cannot view, modify, or delete User B's vault items by manipulating parameter IDs.
- **Role-Based Authorization**:
  - `USER`: Access restricted to personal vault, security health, and standard security tools.
  - `ADMIN`: Access to user management (`/admin/users`) and system audit logs (`/admin/activity`).

---

## 📝 5. Logging & Privacy Policy

PassForge enforces a strict **Zero Secret Payload Disclosure** logging policy:

- **Never Logged**: Plaintext passwords, authentication salts, password hashes, encryption keys, or encrypted vault ciphertexts.
- **Audit Metadata Recorded**: Action event type (`LOGIN_SUCCESS`, `LOGIN_FAILED`, `CREDENTIAL_CREATED`, `USER_ACTIVATED`), timestamp (UTC), user ID, and client IP address.

---

## ⚠️ 6. Threat Model & Educational Limitations

> [!IMPORTANT]
> **Educational Disclaimer**: PassForge is an educational and portfolio project. It has **not** undergone formal independent third-party cryptographic auditing or penetration testing.

- **Compromised Database Scenario**: If the SQLite database is leaked, authentication passwords remain protected by PBKDF2-HMAC-SHA256 (600k iterations), and vault secrets remain protected by AES-128-CBC encryption. Secrets cannot be decrypted without brute-forcing the individual user passwords.
- **Production Guidance**: Real-world production password managers should evaluate memory-hard hashing algorithms such as **Argon2id** (to resist GPU/ASIC brute-forcing) and client-side zero-knowledge encryption in web browsers (e.g. WebCrypto API) before server transmission.

---

## 📬 7. Responsible Disclosure

If you discover any security vulnerabilities or architectural bugs in this educational repository, please open an issue or report via GitHub security advisories.
