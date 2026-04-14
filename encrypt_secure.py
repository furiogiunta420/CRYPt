#!/usr/bin/env python3
"""
Secure Text File Encryptor
Uses Fernet (symmetric encryption) from the cryptography library.

Features:
- AES-128 encryption in CBC mode
- HMAC authentication (detects tampering)
- Random IV for each encryption (same text encrypts differently each time)
- Timestamping
- Password-based key derivation (PBKDF2)
"""

import sys
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from dotenv import load_dotenv 
import os


load_dotenv()


PASSWORD = os.getenv('password')

# Salt for key derivation - keep this consistent between encrypt/decrypt
SALT = b'crypt_asp_fur_oll_420_k6i_o9f'


def derive_key_from_password(password: str) -> bytes:
    """
    Derives a cryptographic key from a password using PBKDF2.
    This makes brute-force attacks much harder.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=480000,  # OWASP recommended minimum (2023)
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_file(input_path: Path, output_path: Path, password: str):
    key = derive_key_from_password(password)
    fernet = Fernet(key)

    with open(input_path, 'rb') as f:
        file_data = f.read()
    
    # Encrypt the data
    # Fernet automatically:
    # - Generates a random IV (initialization vector)
    # - Adds timestamp
    # - Computes HMAC for authentication

    encrypted_data = fernet.encrypt(file_data)

    with open(output_path, 'wb') as f:
        f.write(encrypted_data)
    
    return len(file_data), len(encrypted_data)


def main():
    if len(sys.argv) < 2:
        print("Usage: python encrypt_secure.py <input_file> [output_file]")
        print("Example: python encrypt_secure.py secret.txt secret.encrypted")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.with_suffix(input_file.suffix + '.encrypted')
    
    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found!")
        sys.exit(1)
    
    try:
        original_size, encrypted_size = encrypt_file(input_file, output_file, PASSWORD)
        
        print(f"Secure encryption successful!")
        print(f"Input:     {input_file} ({original_size:,} bytes)")
        print(f"Output:    {output_file} ({encrypted_size:,} bytes)")
        print(f"Algorithm: Fernet (AES-128 CBC + HMAC)")
        print()
        print(f"Keep your password safe! Without it, the file cannot be decrypted.")
        
    except Exception as e:
        print(f"Error during encryption: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
