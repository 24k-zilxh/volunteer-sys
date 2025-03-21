# Package setup - Installs all modules required for it to run
# This will be run when setting it up, and the end user will typically not need to run it
# Includes a GUI, just in case
# if python is upgraded to a later version (3.12.7 -> 3.13.2 for example), you will need to run this again

import subprocess
import customtkinter as ckt # Note that if customtkinter is broken, the pip command will have to be manually entered in the terminal
import shutil
import os

def fixer():
    subprocess.run(["powershell", "-Command", "python -m pip install pandas -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "python -m pip install tabulate -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "python -m pip install customtkinter -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "pip install pillow -q"], capture_output=False) 
    lbll.configure(root, text="all required packages have been reinstalled")

def reset():
    shutil.rmtree(r"\volunteersys")
    os.makedirs(r"\volunteersys")
    lbll.configure(root, text="all data has been reset")

def rm():
    subprocess.run(["powershell", "-Command", "python -m pip install pandas --upgrade -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "python -m pip install tabulate --upgrade -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "python -m pip install customtkinter --upgrade -q"], capture_output=False) 
    subprocess.run(["powershell", "-Command", "pip install pillow --upgrade -q"], capture_output=False) 
    lbll.configure(root, text="upgraded all packages")

root = ckt.CTk()

root.geometry("720x480")
root.title("volunteersys - troubleshooter")

title = ckt.CTkLabel(root, text="volunteer-sys developer tools\nDon't reset unless you have to, all data will be LOST!")
title.pack(padx=10, pady=10)

setup=ckt.CTkButton(root, text="Reinstall Packages",command=fixer,fg_color="#00FF00",text_color="#000000")
setup.pack(padx=10,pady=10)

remove=ckt.CTkButton(root, text="Upgrade Packages",command=rm,fg_color="#008B8B",text_color="#000000")
remove.pack(padx=10,pady=10)

rst=ckt.CTkButton(root, text="Reset",command=reset, fg_color="#FF0000", text_color="#000000")
rst.pack(padx=10,pady=10)

lbll=ckt.CTkLabel(root, text="-----",text_color="#FF474C")
lbll.pack(padx=10,pady=10)

root.mainloop()


