#!/usr/bin/env python3
"""Compatibility entry point; use arch.py or void.py for new installs."""

from pathlib import Path
import runpy

backend = Path(__file__).with_name("arch.py")
runpy.run_path(str(backend), run_name="__main__")
