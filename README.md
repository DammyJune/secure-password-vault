# 🔐 Secure Password Vault

Secure Local Password Manager – Console-based application built with modern cryptography practices.

Student Information  
- Name: Junaid Oluwadamilare Ayomide
- Department: Cybersecurity  
- Matriculation Number: [24/13839]  

Course: (SEN201) Assignment  
Project Focus: Secure credential storage, cryptography basics, threat modeling, and full SDLC implementation  

## Project Overview
This is a console-based password vault that securely stores website credentials using:  
- PBKDF2 key derivation (with salt)  
- Fernet symmetric encryption (AES-128 in CBC + HMAC-SHA256)  
- Never stores the master password in plain text  
- Data encrypted at rest in secure_vault.json  

All names and nomenclatures used in the design match exactly with the implementation:  
- Class: SecureVault  
- Key methods: derive_key(), verify_master_password(), unlock(), add_credential(), get_credential(), list_credentials(), delete_credential()  
- File: secure_vault.json  
- Main functions: load_vault(), save_vault(), set_master_password(), unlock_vault(), display_menu()  

## Features
- Set / change master password (first-time setup)  
- Unlock vault with master password  
- Add website credentials (website, username, password)  
- View specific credential  
- List all stored websites  
- Delete credential  
- Lock vault (clears sensitive data from memory)  
- Persistent encrypted storage  

## Security Design (Consistent Nomenclature)
- salt → Random 16-byte value per vault  
- master_hash → PBKDF2-SHA256 hash of master password (32 bytes)  
- derive_key() → Generates Fernet-compatible key using PBKDF2  
- fernet → Fernet object used for encrypt/decrypt  
- encrypted_data → Base64-encoded encrypted JSON of credentials  
- Memory is cleared on lock/exit (credentials = {} and fernet = None)  

## How to Run
1. Install the required library (only once):
   `bash
   pip install cryptography