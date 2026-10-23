import os
import sys

def change_file(path, symb, symb1):
    with open(path, "r") as r:
        file = r.read()
    new_file = file.replace(symb, symb1)
    with open(path, "w") as w:
        w.write(new_file)

os.system('clear')
print("Welcome to my package manager installer")
choice = input("You want to commit your configuration file on github?[y/n]: ").lower().strip()

if choice == "y":
    user = input("Write your github nickname: ").strip()
    if not user:
        sys.exit()
    repo = input("Write name of repo you want to commit configuration file: ").strip()
    if not repo:
        sys.exit()
    tokken = input("Write your git-token (we will not steal anything from you): ").strip()
    if not tokken:
        sys.exit()

    confirm = input("Directory \"~/.config/dpm\" will be deleted, write [y/n] to confirm: ").lower().strip()
    if confirm == "y":
        os.system("rm -rf ~/.config/dpm")
        os.system("mkdir -p ~/.config/dpm")

        change_file("src/git.py", "GITHUB_USER", user)
        change_file("src/git.py", "GITHUB_REPO", repo)
        change_file("src/git.py", "GITHUB_TOKKEN", tokken)

        os.system("mv src/git.py ~/.config/dpm/main.py")
        os.system("mv src/configuration ~/.config/dpm/configuration")

        os.system("git -C ~/.config/dpm init")

        print("Setting up system command 'dpm'...")

        with open("dpm_launcher", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("python3 ~/.config/dpm/main.py \"$@\"\n")

        os.system("chmod +x dpm_launcher")
        os.system("sudo mv dpm_launcher /usr/local/bin/dpm")

        print("Installation complete with Git support! Type 'dpm' anywhere.")
    else:
        print("Installation aborted.")
        sys.exit()

elif choice == "n":
    print("Ok... without git commit")
    confirm = input("Directory \"~/.config/dpm\" will be deleted, write [y/n] to confirm: ").lower().strip()
    if confirm == "y":
        os.system("rm -rf ~/.config/dpm")
        os.system("mkdir -p ~/.config/dpm")

        os.system("mv src/main.py ~/.config/dpm/main.py")
        os.system("mv src/configuration ~/.config/dpm/configuration")

        print("Setting up system command 'dpm'...")

        with open("dpm_launcher", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("python3 ~/.config/dpm/main.py \"$@\"\n")

        os.system("chmod +x dpm_launcher")
        os.system("sudo mv dpm_launcher /usr/local/bin/dpm")

        print("Installation complete! Type 'dpm' anywhere.")
    else:
        print("Bye..")
        sys.exit()
else:
    print("Invalid option!")
    sys.exit()
