import os
import sys

def change_file(path,symb,symb1):
    with open(path,"r") as r:
        file = r.read()
    new_file = file.replace(symb,symb1)
    with open(path,"w") as w:
        w.write(new_file)

os.system('clear')
print("Welcome to my package manager installer")
passwd = input("[sudo] password").strip()

confirm = input("Directory \"~/.config/dpm\" will be deleted, write [y/n] to confirm: ").lower().strip()
if confirm == "y":
    os.system("rm -rf ~/.config/dpm")
    os.system("mkdir -p ~/.config/dpm")

    change_file("src/main.py","PASSWD",passwd)

    os.system("mv src/main.py ~/.config/dpm/main.py")
    os.system("mv src/configuration ~/.config/dpm/configuration")

    print("Setting up system command 'dpm'...")

    with open("dpm_launcher", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("python3 ~/.config/dpm/main.py \"$@\"\n")

    os.system("chmod +x dpm_launcher")
    os.system(f"echo \"{passwd}\" | sudo -S mv dpm_launcher /usr/local/bin/dpm")
    
    print("Installation complete! Type 'dpm' anywhere.")
else:
    print("Bye..")
    sys.exit()
