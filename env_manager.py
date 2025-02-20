from cryptography.fernet import Fernet
from dotenv import set_key
from config import get_env_variable
import sys

def get_or_set_env_variable(key, prompt_message, is_password=False):
    """
    Get an environment variable, and if not set, prompt the user to set it.
    """
    value = get_env_variable(key)
    if not value:
        if is_password:
            value = Fernet.generate_key().decode()  # Generate a valid Fernet key for encryption
            set_key('.env', key, value)
        else:
            value = input(prompt_message)
            set_key('.env', key, value)
    return value

def get_or_set_encrypted_password(key, fernet):
    """
    Get an encrypted password from the environment variable, and if not set, prompt the user to set it.
    """
    encrypted_password = get_env_variable(key)
    if not encrypted_password:
        password = input("Set a password: ").encode()  # Convert input to bytes
        encrypted_password = fernet.encrypt(password).decode()  # Encrypt and convert to string
        set_key('.env', key, encrypted_password)
        print("Password set and stored successfully.")
    else:
        encrypted_password = encrypted_password.encode()  # Convert to bytes
        password = fernet.decrypt(encrypted_password).decode()  # Decrypt and convert to string
        user_input = input("Enter the password: ")
        if user_input != password:
            print("Incorrect password.")
            sys.exit(1)
    return encrypted_password