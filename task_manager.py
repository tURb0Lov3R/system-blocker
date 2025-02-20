import os
import subprocess

def create_batch_file():
    #Create a batch file to run the Python script.

    batch_file_path = "run_script.bat"
    script_path = os.path.abspath(__file__)
    with open(batch_file_path, "w") as batch_file:
        batch_file.write(f'@echo off\npython "{script_path}"\n')
    return batch_file_path

def create_scheduled_task(batch_file_path):
    #Create a scheduled task to run the batch file on user logon.

    task_name = "SystemBlockerScript"
    command = f'schtasks /create /tn "{task_name}" /tr "{batch_file_path}" /sc onlogon /rl highest /f'
    subprocess.call(command, shell=True)