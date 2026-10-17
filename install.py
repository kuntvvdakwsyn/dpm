import os
import sys

os.system('clear')
print("Welcome to my package manager installer")
choice = input("Directory \"~/.config/dpm\" will be deleted, write [y/n] to confirm: ").lower()

if choice == "y":
    os.system("rm -rf ~/.config/dpm")
    os.system("mkdir -p ~/.config/dpm")
    os.system("mv src/configuration src/main.py ~/.config/dpm/")
    
    print("Setting up system command 'dpm'...")
    
    with open("dpm_launcher", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("python3 ~/.config/dpm/main.py \"$@\"\n")
    
    os.system("chmod +x dpm_launcher")
    os.system("sudo mv dpm_launcher /usr/local/bin/dpm")
    
    print("Installation complete! You can now just type 'dpm' anywhere in your terminal.")

elif choice == "n":
    print("Bye..")
else:
    print("Invalid option!")
    sys.exit()