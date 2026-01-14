import json
import os
import base64
from getpass import getpass
from cryptography.fernet import Fernet, InvalidToken
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

VAULT_FILE = "secure_vault.json"
backend = default_backend()

class SecureVault:
    def __init__(self):
        self.master_hash = None
        self.salt = None
        self.credentials = {}       # plaintext only in memory after unlock
        self.fernet = None

    def derive_key(self, master_password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100_000,
            backend=backend
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    def verify_master_password(self, password: str) -> bool:
        if self.master_hash is None:
            return False
        key = self.derive_key(password)
        test_fernet = Fernet(key)
        try:
            test_fernet.decrypt(b"test")  # dummy - we just need object
            return True
        except:
            return False

    def unlock(self, master_password: str) -> bool:
        if not self.verify_master_password(master_password):
            return False
        self.fernet = Fernet(self.derive_key(master_password))
        return True

    def add_credential(self, website: str, username: str, password: str):
        self.credentials[website.lower()] = {"username": username, "password": password}
        print(f"Credential for {website} added.")

    def get_credential(self, website: str):
        site = website.lower()
        if site in self.credentials:
            cred = self.credentials[site]
            print(f"\nWebsite : {website}")
            print(f"Username: {cred['username']}")
            print(f"Password: {cred['password']}")
        else:
            print("No credential found for that website.")

    def list_credentials(self):
        if not self.credentials:
            print("No credentials stored yet.")
            return
        print("\nStored websites:")
        for site in sorted(self.credentials.keys()):
            print(f"• {site}")

    def delete_credential(self, website: str):
        site = website.lower()
        if site in self.credentials:
            del self.credentials[site]
            print(f"Credential for {website} deleted.")
        else:
            print("Credential not found.")

def load_vault():
    vault = SecureVault()
    if not os.path.exists(VAULT_FILE):
        return vault

    try:
        with open(VAULT_FILE, "r") as f:
            data = json.load(f)
        vault.salt = base64.urlsafe_b64decode(data["salt"])
        vault.master_hash = base64.urlsafe_b64decode(data["master_hash"])
        # encrypted_data will be decrypted only after unlock
        vault.encrypted_data = base64.urlsafe_b64decode(data.get("encrypted_data", "e30="))  # empty dict default
    except:
        print("Vault file corrupted. Starting fresh.")
    return vault

def save_vault(vault: SecureVault):
    if vault.fernet is None:
        print("Vault not unlocked - cannot save.")
        return

    try:
        encrypted = vault.fernet.encrypt(json.dumps(vault.credentials).encode())
        data = {
            "salt": base64.urlsafe_b64encode(vault.salt).decode(),
            "master_hash": base64.urlsafe_b64encode(vault.master_hash).decode(),
            "encrypted_data": base64.urlsafe_b64encode(encrypted).decode()
        }
        with open(VAULT_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print("Vault saved securely.")
    except Exception as e:
        print(f"Save error: {e}")

def set_master_password(vault: SecureVault):
    if vault.master_hash is not None:
        print("Master password already set.")
        return
    password = getpass("Set your master password: ")
    confirm = getpass("Confirm master password: ")
    if password != confirm:
        print("Passwords do not match!")
        return
    vault.salt = os.urandom(16)
    vault.master_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), vault.salt, 100_000, 32)
    vault.credentials = {}
    vault.fernet = Fernet(vault.derive_key(password))
    print("Master password set successfully.")

def unlock_vault(vault: SecureVault) -> bool:
    if vault.master_hash is None:
        print("No vault found. Set master password first.")
        return False
    password = getpass("Enter master password: ")
    if vault.unlock(password):
        try:
            decrypted = vault.fernet.decrypt(vault.encrypted_data)
            vault.credentials = json.loads(decrypted)
            print("Vault unlocked successfully.")
            return True
        except InvalidToken:
            print("Decryption failed - wrong master password?")
            return False
    else:
        print("Incorrect master password.")
        return False

def display_menu(locked: bool):
    print("\n" + "═"*50)
    print("      SECURE PASSWORD VAULT")
    print("═"*50)
    if locked:
        print("1. Unlock Vault")
        print("2. Set Master Password (first time)")
        print("3. Exit")
    else:
        print("1. Add Credential")
        print("2. View Credential")
        print("3. List All Websites")
        print("4. Delete Credential")
        print("5. Lock Vault")
        print("6. Exit")
    print("═"*50)

def main():
    vault = load_vault()
    locked = True

    while True:
        display_menu(locked)
        choice = input("Choose option: ").strip()

        if locked:
            if choice == "1":
                if unlock_vault(vault):
                    locked = False
            elif choice == "2":
                set_master_password(vault)
                if vault.master_hash is not None:
                    locked = False  # auto-unlock after setting
            elif choice == "3":
                print("Goodbye.")
                break
        else:
            if choice == "1":
                website = input("Website: ").strip()
                username = input("Username/email: ").strip()
                password = getpass("Password: ")
                vault.add_credential(website, username, password)
            elif choice == "2":
                website = input("Website to view: ").strip()
                vault.get_credential(website)
            elif choice == "3":
                vault.list_credentials()
            elif choice == "4":
                website = input("Website to delete: ").strip()
                vault.delete_credential(website)
            elif choice == "5":
                save_vault(vault)
                vault.credentials = {}  # clear memory
                vault.fernet = None
                locked = True
                print("Vault locked.")
            elif choice == "6":
                save_vault(vault)
                print("Securely exiting. Stay safe!")
                break

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # clean screen
    print("Secure Password Vault - Protect your credentials\n")
    main()
