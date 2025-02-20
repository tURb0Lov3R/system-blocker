import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_env_variable(key, default=None):
    return os.getenv(key, default)