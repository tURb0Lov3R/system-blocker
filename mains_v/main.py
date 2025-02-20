import sys
import subprocess
import os
from cryptography.fernet import Fernet
from key_manager import store_key, retrieve_key
import logging
from utils import check_and_install_package, is_within_timeframe
from env_manager import get_or_set_env_variable, get_or_set_encrypted_password
from task_manager import create_batch_file, create_scheduled_task

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check and install required packages
check_and_install_package('cryptography')
check_and_install_package('python-dotenv')
check_and_install_package('pywin32', 'win32api')

def change_user_password(username, new_password):
    """
    Change the Windows user password.
    """
    command = f'net user {username} {new_password}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to change password: {result.stderr}")

def main():
    # Check if the key is already stored in the .env file
    key = get_or_set_env_variable("FERNET_KEY", "Generated and stored key: ", is_password=True)
    key = key.encode()  # Convert the key to bytes
    print(f"Retrieved key: {key}")

    start = get_or_set_env_variable("SET_START_TIME", "Insert start time (HH:MM): ")
    end = get_or_set_env_variable("SET_END_TIME", "Insert end time (HH:MM): ")
    f = Fernet(key)  # Using key for encryption

    # Check if password is already set in the .env file
    encrypted_password = get_or_set_encrypted_password("ENCRYPTED_PASSWORD", f)

    if not is_within_timeframe(start, end):
        print("The system is not available at this time.")
        # Block the user access
        input("Blocking user access...")
        # Decrypt the password
        decrypted_password = f.decrypt(encrypted_password.encode()).decode()
        # Change the user password
        username = os.getlogin()
        change_user_password(username, decrypted_password)
        # Log the user out
        subprocess.call(["shutdown", "/l"])
        sys.exit(1)

    try:
        input("User access is allowed.")
        key = retrieve_key(get_or_set_env_variable("MY_SECURE_KEY_APP", "Enter your secure key app: "))
        if not key:
            raise Exception("Key not found")

        # Allow the user access
        print("Allowing user access")
    except Exception as e:
        input(f"Error retrieving key: {e}")
        sys.exit(1)
    
    input("Blocker is running...")

if __name__ == "__main__":
    # Check if the batch file and scheduled task exist, if not, create them
    batch_file_path = "run_script.bat"
    task_name = "SystemBlockerScript"
    if not os.path.exists(batch_file_path):
        batch_file_path = create_batch_file()
    if subprocess.call(f'schtasks /query /tn "{task_name}"', shell=True) != 0:
        create_scheduled_task(batch_file_path)
    
    main()