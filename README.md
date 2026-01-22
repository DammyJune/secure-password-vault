Secure Password Vault - SDLC Project

A Console-Based Password Manager Following Full Software Development Life Cycle

Student Information

Name: Junaid Oluwadamilare Ayomide
Department: Cybersecurity
Matric Number: [24/13839]
Course: SEN201 Assignment
Project Focus: Secure credential storage, cryptography implementation, threat modeling, and complete SDLC demonstration

Project Overview

This is a console-based password manager that securely stores website credentials using modern cryptography. The project was developed following all phases of the Software Development Life Cycle (SDLC) to demonstrate proper software engineering practices.

SDLC Phases Implementation

Phase 1: Planning and Requirements Analysis

I began by identifying what the password vault needed to do:

· Store website credentials (website, username, password) securely
· Protect access with a master password
· Allow users to add, view, and delete credentials
· Ensure all data remains encrypted when stored
· Clear sensitive information from memory when not in use

Phase 2: System Design

I designed the system architecture:

· Console-based interface for simplicity
· JSON file for encrypted storage
· Cryptographic components:
  · PBKDF2 for key derivation (slows down password guessing)
  · Fernet encryption (AES-128 with HMAC validation)
  · Random salt for each vault
· Class structure with SecureVault as the main component
· Methods for unlock, add, get, list, and delete operations

Phase 3: Implementation

I wrote the Python code with these key components:

· Main program file: secure_vault.py
· Data storage file: secure_vault.json
· Core functions:
  · derive_key(): Creates encryption key from master password
  · verify_master_password(): Validates user's password
  · add_credential(): Stores new website credentials
  · get_credential(): Retrieves specific credentials
  · list_credentials(): Shows all stored websites
  · delete_credential(): Removes stored credentials

Phase 4: Testing

I tested the application thoroughly:

· First-time setup and master password creation
· Valid and invalid password attempts
· Adding and retrieving credentials
· File persistence (data survives program restart)
· Memory clearance (no passwords left in memory)
· Error handling for file operations

Phase 5: Deployment

The application runs locally and requires:

1. Python 3.x installed
2. Cryptography library: pip install cryptography
3. Running the program: python secure_vault.py

Phase 6: Maintenance

Future improvements could include:

· Password strength checking
· Automatic lock after inactivity
· Backup and restore functionality
· Password generation feature

Security Features

· No master password stored anywhere
· All data encrypted before saving to file
· Each vault gets unique random salt
· Encryption uses industry-standard algorithms
· Memory cleared when vault is locked or program exits
· Encrypted file format prevents casual inspection

How to Use

1. First run: Set your master password
2. Unlock the vault with your master password
3. Use the menu to:
   · Add new website credentials
   · View stored credentials
   · List all websites
   · Delete credentials
   · Lock the vault when done

Files in the Project

· secure_vault.py - Main program
· secure_vault.json - Encrypted data storage
· README.md - This documentation

Important Notes

· This is an educational project for SEN201 course
· The master password cannot be recovered if forgotten
· Keep a backup of your secure_vault.json file
· While using strong cryptography, this is not intended for highly sensitive real-world use

Learning Outcomes

Through this project, I applied:

· Software Development Life Cycle methodology
· Cryptographic principles and implementation
· Secure programming practices
· Threat modeling for password storage
· Python programming and file handling
· Error handling and user interface design


Project developed as part of Cybersecurity coursework, demonstrating practical application of SDLC and security principles.