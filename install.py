#!/usr/bin/env python3
"""Install DPM for Arch Linux or Void Linux."""

import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "src"
CONFIG_DIR = Path.home() / ".config" / "dpm"


def choose_distro():
    while True:
        distro = input("Which distribution are you using? [arch/void]: ").strip().lower()
        if distro in {"arch", "void"}:
            return distro
        print("Please enter 'arch' or 'void'.")


def main():
    distro = choose_distro()
    source = SOURCE_DIR / f"{distro}.py"
    if not source.is_file():
        raise SystemExit(f"Backend not found: {source}")

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, CONFIG_DIR / f"{distro}.py")
    # Keep the existing package list instead of deleting the user's configuration.
    config_file = CONFIG_DIR / "configuration"
    if not config_file.exists():
        shutil.copy2(SOURCE_DIR / "configuration", config_file)

    launcher = f"#!/bin/sh\nexec python3 \"$HOME/.config/dpm/{distro}.py\" \"$@\"\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
        handle.write(launcher)
        launcher_path = Path(handle.name)

    try:
        subprocess.run(["sudo", "install", "-m", "755", str(launcher_path), "/usr/local/bin/dpm"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        raise SystemExit(f"Could not install /usr/local/bin/dpm: {error}") from error
    finally:
        launcher_path.unlink(missing_ok=True)

    print(f"DPM installed for {distro.title()}. Run 'dpm' to start it.")


if __name__ == "__main__":
    main()
