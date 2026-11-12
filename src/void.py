#!/usr/bin/env python3
"""Interactive package helper for Void Linux (XBPS)."""

import subprocess
import sys
from pathlib import Path

CONFIG_FILE = Path.home() / ".config" / "dpm" / "configuration"


def packages_from_input(prompt):
    return input(prompt).split()


def run_command(command):
    try:
        return subprocess.run(command, check=False).returncode == 0
    except FileNotFoundError:
        print(f"Command not found: {command[0]}")
        return False


def save_package(package):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = CONFIG_FILE.read_text().splitlines() if CONFIG_FILE.exists() else []
    if package not in existing:
        with CONFIG_FILE.open("a", encoding="utf-8") as config:
            config.write(("\n" if existing else "") + package + "\n")


def remove_package_from_config(package):
    if not CONFIG_FILE.exists():
        return
    lines = [line for line in CONFIG_FILE.read_text().splitlines() if line.strip() != package]
    CONFIG_FILE.write_text("".join(f"{line}\n" for line in lines), encoding="utf-8")


def install():
    for package in packages_from_input("Packages to install (space-separated): "):
        if run_command(["sudo", "xbps-install", "-S", "-y", package]):
            save_package(package)


def delete():
    for package in packages_from_input("Packages to remove (space-separated): "):
        if run_command(["sudo", "xbps-remove", "-R", "-y", package]):
            remove_package_from_config(package)


def check():
    if not CONFIG_FILE.exists():
        print("No package configuration found yet.")
        return
    print(CONFIG_FILE.read_text(encoding="utf-8"), end="")


def sync():
    if not CONFIG_FILE.exists():
        print("No package configuration found yet.")
        return
    packages = [line.strip() for line in CONFIG_FILE.read_text().splitlines() if line.strip()]
    if packages:
        run_command(["sudo", "xbps-install", "-S", "-y", *packages])


def main():
    while True:
        print("\nDPM — Void Linux (XBPS)\n1. Install packages\n2. Remove packages\n3. Show saved packages\n4. Sync saved packages\n5. Quit")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            install()
        elif choice == "2":
            delete()
        elif choice == "3":
            check()
        elif choice == "4":
            sync()
        elif choice == "5":
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)
