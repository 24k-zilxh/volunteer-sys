# Package setup - Installs all modules required for it to run
# This will be run when setting it up, and the end user will typically not need to run it
# Includes a GUI, just in case
# if python is upgraded to a later version (3.12.7 -> 3.13.2 for example), you will need to run this again
# unless you really need to, just stay on 3.12.7 - i did most of the testing on this python version

import subprocess
import customtkinter as ckt # Note that if customtkinter is broken, the pip command will have to be manually entered in the terminal
import shutil
import os
import logging


logging.disable(logging.CRITICAL) # Turning off all outputs to cmd



def fixer():
    subprocess.run(["powershell", "-Command", "python -m pip uninstall pandas -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "python -m pip uninstall tabulate -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "pip uninstall pillow -q"], capture_output=False) 

    subprocess.run(["powershell", "-Command", "python -m pip install pandas -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "python -m pip install tabulate -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "python -m pip install customtkinter -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "pip install pillow -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "pip install psutil -q"], capture_output=False) 

    lbll.configure(root, text="all required packages have been reinstalled")

def reset():
    shutil.rmtree(r"\volunteersys")
    os.makedirs(r"\volunteersys")
    os.makedirs(r"\volunteersys\vol_files")
    lbll.configure(root, text="all data has been reset")

def update():
    subprocess.run(["powershell", "-Command", "python -m pip install --upgrade pandas -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "python -m pip install --upgrade tabulate -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "python -m pip install --upgrade customtkinter -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "pip install --upgrade pillow -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "pip install --upgrade psutil -q"], capture_output=False) 

    lbll.configure(root, text="all required packages have been updated")

def storage_dirs():
    lbll.configure("entering the folder with all files\nbe careful, you might corrupt the data")

    os.startfile(r"\volunteersys")


root = ckt.CTk()

root.geometry("720x480")
root.title("VOLUNTEERSYS - DEVELOPER MENU")

title = ckt.CTkLabel(root, text="VOLUNTEER-SYS DEVELOPER MENU")
title.pack(padx=10, pady=10)

setup=ckt.CTkButton(root, text="Reinstall Packages",command=fixer,fg_color="#00CC00",text_color="#000000")
setup.pack(padx=10,pady=10)

remove=ckt.CTkButton(root, text="Upgrade Packages",command=update,fg_color="#008B8B",text_color="#000000")
remove.pack(padx=10,pady=10)

dirview = ckt.CTkButton(root,text="Storage Directory",command=storage_dirs)
dirview.pack(padx=10,pady=10)

rst=ckt.CTkButton(root, text="Reset",command=reset, fg_color="#FF0000", text_color="#000000")
rst.pack(padx=10,pady=10)

lbll=ckt.CTkLabel(root, text="-----",text_color="#FF474C",font=("Arial",40))
lbll.pack(padx=10,pady=10)

root.mainloop()