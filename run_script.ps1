$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
python.exe "$scriptDir\secure-script.py"