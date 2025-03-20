# Package setup - Installs all modules required for it to run
# This will be run when setting it up, and the end user will typically not need to run it
# if python is updated to a later version (3.12.7 -> 3.13.2 for example), you will need to run this again

import subprocess

subprocess.run(["powershell", "-Command", "python -m pip install pandas"], capture_output=False) 
subprocess.run(["powershell", "-Command", "python -m pip install tabulate"], capture_output=False) 
subprocess.run(["powershell", "-Command", "python -m pip install customtkinter"], capture_output=False) 
subprocess.run(["powershell", "-Command", "pip install pillow"], capture_output=False) 
