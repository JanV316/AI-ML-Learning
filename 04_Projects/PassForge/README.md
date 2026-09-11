# PassForge — Privacy-Focused Password Security & Credential Vault

**PassForge** is a privacy-focused password security toolkit and personal credential vault. Built in Python and Flask, PassForge provides secure random password generation, multi-word passphrase creation, rule-based weakness analysis, theoretical entropy estimation, PBKDF2-HMAC-SHA256 password hashing, and Fernet-encrypted credential storage.

---

## 📋 Problem & Overview

### The Problem
- **Weak Passwords**: Users frequently choose predictable passwords susceptible to dictionary and brute-force attacks.
- **Password Reuse**: Reusing identical passwords across multiple websites means a single breach compromises all accounts.
- **Unencrypted Credential Storage**: Storing passwords in plaintext files, notes, or browser memory leaves credentials vulnerable to unauthorized access.
- **Lack of Visibility**: Users lack quantitative feedback regarding password strength, bit entropy, and vulnerability patterns.

### How PassForge Solves It
- **Cryptographic Random Generation**: Generates randomized passwords using Python's `secrets` module with custom character set controls or multi-word Diceware passphrases.
- **Rule-Based Analysis & Entropy**: Evaluates length, character diversity, dictionary matches, repeated characters, and calculates theoretical bit entropy ($E = L \times \log_2(R)$).
- **Zero-Knowledge Credential Vault**: Encrypts saved vault credentials symmetrically using **Fernet (AES-128-CBC + HMAC-SHA256)** keys derived in-memory per user session.
- **Password Health Monitoring**: Identifies weak passwords and detects password reuse across saved vault items.
- **Role-Based Security Audit Logs**: Records audit events (`LOGIN_SUCCESS`, `CREDENTIAL_CREATED`, `USER_ACTIVATED`) without logging passwords, salts, or encryption keys.

---

## ✨ Features

- **🔑 Password & Passphrase Generator**: Cryptographically secure random generation via `secrets` module. Supports custom length, uppercase, lowercase, numbers, symbols, and multi-word passphrases with an optional "Save to Vault" workflow.
- **📊 Local Strength & Entropy Analyzer**: Rule-based scoring, entropy estimation in bits, dictionary checking, repeated/sequential pattern detection, and actionable suggestions.
- **🔒 PBKDF2 Password Hashing**: Derives authentication hashes using `PBKDF2-HMAC-SHA256` with 600,000 iterations and 16-byte random salts.
- **✅ Constant-Time Hash Verification**: Uses `hmac.compare_digest()` to prevent timing side-channel attacks.
- **🛡️ Encrypted Credential Vault**: Symmetrically encrypts stored website logins per user. Supports search filtering, masked display (`••••••••••••`), secure reveal toggles, and copy controls.
- **🩺 Password Health Assessment**: Computes vault health scores (0–100) and detects password reuse across saved services.
- **👥 Role-Based Access & Admin Panel**: `USER` vs `ADMIN` roles. Administrators can manage account activation and view audit activity logs without accessing users' vault contents.
- **💻 Dual Web & CLI Interfaces**: Accessible via modern Flask web interface or full terminal CLI subcommands.

---

## 🏗️ System Architecture

```text
                           BROWSER (Dark Graphite Charcoal UI)
                                            │
                                            ▼
                              FLASK WEB APPLICATION (web.py)
                        ┌───────────────────┴───────────────────┐
                        ▼                                       ▼
               AUTH & VAULT MODULES                    SECURITY TOOLKIT
              ├── auth.py                              ├── generator.py
              ├── vault.py                             ├── analyzer.py
              └── models.py                            └── security.py
                        │
                        ▼
              SQLITE DB (passforge.db)
```

### Security Model: Hashing vs. Encryption

| Operation | Target Data | Technology Used | Storage & Lifetime |
| :--- | :--- | :--- | :--- |
| **Authentication Hashing** | User Login Password | `PBKDF2-HMAC-SHA256` (600k iterations + 16-byte salt) | Salt & Hash stored in `users` table. **One-way (irreversible)**. |
| **Vault Secret Encryption** | Saved Service Passwords | `Fernet` (AES-128-CBC + HMAC-SHA256) | Ciphertext stored in `credentials` table. Key exists **only in active session memory**. |

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, Flask
- **Database**: SQLite3
- **Cryptography**: Python Standard Library (`secrets`, `hashlib`, `hmac`, `base64`) & `cryptography`
- **Frontend**: HTML5, Custom CSS (`static/css/style.css`), Vanilla JavaScript (`static/js/app.js`)
- **Testing**: `unittest`

---

## 🚀 Installation & Running

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/JanV316/PassForge.git
cd PassForge
pip install -r requirements.txt
```

### 2. Start the Web Application

Launch the Flask web server:

```bash
python main.py --web
# OR
python -m passforge.web
```

Open your browser and navigate to: **`http://127.0.0.1:5000`**

### 3. Run Terminal CLI Interface

```bash
python main.py
# OR
python -m passforge generate --length 20
python -m passforge analyze
```

---

## 🧪 Testing

PassForge contains an automated unit test suite covering password generation, rule analysis, hashing, encryption, authentication, vault CRUD, CLI commands, and Flask endpoints.

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

- **Test Suite Result**: **53 tests passed** out of 53 tests.

---

## 🖼️ User Interface Highlights

- **Dashboard**: Personal Security Overview showing total saved credentials, strong/weak counts, and items needing attention.
- **Vault**: Searchable list of saved logins with masked password fields, reveal toggles, and copy controls.
- **Generator**: Interactive generator supporting custom length, character toggles, passphrase mode, and optional vault saving.
- **Analyzer**: Comprehensive score bar, theoretical entropy metrics, character set flags, and risk warnings.
- **Admin Panel**: Role-protected dashboard for account management and security audit logging.

---

## ⚠️ Limitations & Educational Disclosures

> [!IMPORTANT]
> **Educational Disclaimer**: PassForge is developed as an educational and portfolio project. It has not undergone third-party penetration testing or formal security audits.

- **Rule-Based Heuristic**: Strength scoring is based on heuristics and pool entropy; it does not replace deep statistical models like `zxcvbn`.
- **In-Memory Vault Keys**: Encryption keys reside in server session memory during active login. Production applications should evaluate client-side WebCrypto encryption.

---

## 🔮 Future Improvements

- Multi-Factor Authentication (MFA / TOTP)
- Client-side WebCrypto browser-based vault key derivation
- Support for FIDO2 / Passkey authentication
- Hardware security key integration
