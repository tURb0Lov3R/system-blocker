import win32cred
import base64

def store_key(name, app_name, key):
    credential = {
        'Type': win32cred.CRED_TYPE_GENERIC,
        'TargetName': name,
        'UserName': app_name,
        'CredentialBlob': base64.urlsafe_b64encode(key).decode('utf-8'),  # Encode to base64 and decode to string
        'Persist': win32cred.CRED_PERSIST_LOCAL_MACHINE
    }
    win32cred.CredWrite(credential, 0)

def retrieve_key(name):
    try:
        creds = win32cred.CredRead(name, win32cred.CRED_TYPE_GENERIC)
        key = creds['CredentialBlob']
        # Add padding if necessary
        missing_padding = len(key) % 4
        if missing_padding:
            key += '=' * (4 - missing_padding)
        return base64.urlsafe_b64decode(key)  # Decode from base64
    except Exception as e:
        raise Exception(f"Error retrieving credentials: {e}")