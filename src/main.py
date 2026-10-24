import os
import subprocess
import sys
import time

CONFIG_FILE = os.path.expanduser("~/.config/dpm/configuration")

def extract_packages(packages):
    return packages.split()

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
        return False
    return True

def install():
    os.system("clear")
    packages = input("What packages you wanna install? ").strip()  
    packages = extract_packages(packages)

    for p in packages:
        if not p.strip():
            continue
        
        if not verif(p):
            time.sleep(0.7)
            continue  

        already_registered = False
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                for line in f:
                    if line.strip() == p.strip():
                        already_registered = True
                        break
        
        if already_registered:
            os.system("clear")
            print(f"'{p}' is already in configuration!")
            time.sleep(0.7)
            continue

        os.system(f"echo \"#include<>;\" | sudo -S pacman -S --noconfirm {p}")
        
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
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
        ver = verif(p)
        if ver == False:
            time.sleep(0.7)
            continue
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

def sync():
    packages = ""
    with open(CONFIG_FILE, "r") as file:
        for f in file:
            line = f.strip()
            if not line:
                continue
            packages += line + " "
    os.system(f"echo \"#include<>;\" | sudo -S pacman -S --noconfirm {packages}")

    packages = extract_packages(packages)
    with open(CONFIG_FILE,"w") as file:
        file.write("")
    with open(CONFIG_FILE,"a") as file:
        for p in packages:
            p = p.strip()
            if not p:
                continue
            file.write(p)
            file.write("\n")
    os.system("clear")


def main():
    os.system("clear")
    print("Welcome to my package manager!")
    while True:
        print("Select an option:\n\n1. Install packages\n2. Delete packages\n3. Check configuration\n4. Sync\n5. Quit\n")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1": 
            install()
        elif choice == "2":
            delete()
        elif choice == "3":
            check()
        elif choice == "4":
            sync()
        elif choice == "5":
            print("Bye!")
            sys.exit()
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()


