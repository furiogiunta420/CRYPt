import sys
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from dotenv import load_dotenv
import os 




load_dotenv()


PASSWORD = os.getenv('password')

# Salt - must match the encryption script
SALT = b'crypt_asp_fur_oll_420_k6i_o9f'


def derive_key_from_password(password: str) -> bytes:
    """
    Derives a cryptographic key from a password using PBKDF2.
    Must use same parameters as encryption.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def decrypt_file(input_path: Path, output_path: Path, password: str):

    key = derive_key_from_password(password)
    fernet = Fernet(key)
    

    with open(input_path, 'rb') as f:
        encrypted_data = f.read()
    
    # Decrypt the data
    # Fernet automatically:
    # - Verifies the HMAC (authentication)
    # - Checks the timestamp
    # - Decrypts the data
    # If any of these fail, InvalidToken exception is raised
    decrypted_data = fernet.decrypt(encrypted_data)
    
    
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)
    
    return len(encrypted_data), len(decrypted_data)


def main():
    if len(sys.argv) < 2:
        print("Usage: python decrypt_secure.py <encrypted_file> [output_file]")
        print("Example: python decrypt_secure.py secret.encrypted secret_restored.txt")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    
    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        if input_file.suffix == '.encrypted':
            output_file = input_file.with_suffix('')
        else:
            output_file = input_file.with_stem(f"{input_file.stem}_decrypted")
    
    
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found!")
        sys.exit(1)
    
    try:
        encrypted_size, decrypted_size = decrypt_file(input_file, output_file, PASSWORD)
        
        print(f"✓ Secure decryption successful!")
        print(f"Input:     {input_file} ({encrypted_size:,} bytes)")
        print(f"Output:    {output_file} ({decrypted_size:,} bytes)")
        print(f"Algorithm: Fernet (AES-128 CBC + HMAC)")
        
    except InvalidToken:
        print(f"Decryption failed!")
        print(f"Possible reasons:")
        print(f"- Wrong password")
        print(f"- File has been tampered with")
        print(f"- File was not encrypted with this tool")
        print(f"- Corrupted file")
        sys.exit(1)
    except Exception as e:
        print(f"Error during decryption: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
