import os
import subprocess
import sys
import time

CONFIG_FILE = os.path.expanduser("~/.config/dpm/configuration")

def extract_packages(pack):
    packages = [""]
    index = 0 
    for p in range(len(pack)):
        if pack[p] == " ":
            index += 1
            packages.append("")
        else:
            packages[index] += pack[p]
    return packages

def verif_installed(package):
    if not package.strip():
        return

    rezultat = subprocess.run(
        ["pacman", "-Q", package],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if rezultat.returncode != 0:
        print(f"'{package}' don`t installed!")
        sys.exit()

def verif(package):
    if not package.strip():
        return 

    rezultat = subprocess.run(
        ["pacman", "-Si", package],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if rezultat.returncode != 0:
        print(f"{package} don`t exist")
        sys.exit()

def install():
    os.system("clear")
    packages = input("What packages you wanna install? ").strip() 
    packages = extract_packages(packages)

    for p in packages:
        if not p.strip():
            continue
        verif(p)

        already_registered = False
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() == p.strip():
                        already_registered = True
                        break
        
        if already_registered:
            os.system("clear")
            print(f"'{p}' is already in configuration!")
            time.sleep(0.7)
            continue
        os.system(f"echo \"#include<>;\" | sudo -S pacman -S --noconfirm {p}")
        with open(CONFIG_FILE, "a") as f:
            f.write(f"\n{p}") 
    os.system("clear")

def delete():
    os.system("clear")
    packages = input("What packages you wanna delete? ").strip()
    packages = extract_packages(packages)
    if not packages:
        sys.exit()
    for p in packages:
        verif(p)
        verif_installed(p)
        os.system(f"echo \"#include<>;\" | sudo -S pacman -Rns --noconfirm {p}")

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                lines = f.readlines()

            with open(CONFIG_FILE, "w") as f:
                for line in lines:
                    if line.strip() != p.strip():
                        f.write(line)
        else:
            print(f"Failed to open {CONFIG_FILE} file")
            sys.exit()

def check():
    os.system(f"less {CONFIG_FILE}")
    os.system("clear")

def main():
    os.system("clear")
    print("Welcome to my package manager!")
    while True:
        print("Select an option:\n\n1. Install packages\n2. Delete packages\n3. Check configuration\n4. Quit\n")
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            install()
        elif choice == "2":
            delete()
        elif choice == "3":
            check()
        elif choice == "4":
            print("Bye!")
            sys.exit()
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
