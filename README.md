# 🔐 Secure Password Vault

Console-based password manager built with cryptography best practices.  
Project created by a female cybersecurity student to demonstrate secure credential storage in the SDLC context.

## Security Features
- PBKDF2-SHA256 key derivation (100,000 iterations)
- Fernet (AES-128 + HMAC-SHA256) symmetric encryption
- Never stores master password
- Salted hashing
- Memory cleaning on lock/exit

## How to Run
```bash
pip install cryptography
python secure_vault.py

class SecureVault:
    • master_key_hash     (bytes)          # PBKDF2 of master password
    • salt                (bytes)
    • credentials         (dict)           # website → {"username": str, "password": str (plaintext in memory only)}
    
    Methods (exact names used in code):
    • derive_key(master_password) → Fernet key
    • verify_master_password(password) → bool
    • add_credential(website, username, password)
    • get_credential(website)
    • delete_credential(website)
    • list_all_websites()
