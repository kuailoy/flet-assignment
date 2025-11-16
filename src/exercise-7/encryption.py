import os
from flet.security import encrypt, decrypt

def encrypt_message(message: str, passphrase: str) -> str:
    # Use passphrase as secret key (first 32 chars)
    secret_key = passphrase.ljust(32)[:32]
    return encrypt(message, secret_key)

def decrypt_message(encrypted_data: str, passphrase: str) -> str:
    secret_key = passphrase.ljust(32)[:32]
    try:
        return decrypt(encrypted_data, secret_key)
    except Exception:
        return "[Unable to decrypt - wrong passphrase?]"