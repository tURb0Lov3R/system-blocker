import subprocess
import sys
import datetime
import os
from dotenv import set_key

def check_and_install_package(package, module_name=None):
    if module_name is None:
        module_name = package

    installed_packages = os.getenv("INSTALLED_PACKAGES", "").split(",")

    if package in installed_packages:
        print(f"{package} is already installed.")
        return

    try:
        __import__(module_name)
    except ImportError:
        response = input(f"{package} is not installed. Do you want to install it? (y/n): ")
        if response.lower() == 'y':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"{package} installed successfully.")
                if package == 'pywin32':
                    # Additional step for pywin32
                    try:
                        subprocess.check_call([sys.executable, "-m", "pywin32_postinstall", "-install"])
                        print("pywin32 post-install script executed successfully.")
                    except subprocess.CalledProcessError as e:
                        input(f"Failed to execute pywin32 post-install script: {e}")
                        sys.exit(1)
                # Update the .env file with the installed package
                installed_packages.append(package)
                set_key('.env', 'INSTALLED_PACKAGES', ",".join(installed_packages))
            except subprocess.CalledProcessError as e:
                input(f"Failed to install {package}: {e}")
                sys.exit(1)
        else:
            input("Exiting the script")
            sys.exit(1)

def is_within_timeframe(start, end):
    now = datetime.datetime.now().time()
    start = datetime.datetime.strptime(start, "%H:%M").time()   # HH:MM format
    end = datetime.datetime.strptime(end, "%H:%M").time()

    current_time = now

    if start <= end:
        return start <= current_time <= end
    else:
        return current_time >= start or current_time <= end