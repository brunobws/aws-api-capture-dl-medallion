#!/usr/bin/env python3
"""
Bootstrap script to create the project structure and generate all files.
Run this once to set up the modular dashboard.
"""

import os
from pathlib import Path

# Define base directory
BASE_DIR = Path(__file__).parent

# Create directory structure
DIRS_TO_CREATE = [
    BASE_DIR / "services",
    BASE_DIR / "pages",
    BASE_DIR / "components",
]

for directory in DIRS_TO_CREATE:
    directory.mkdir(parents=True, exist_ok=True)
    print(f"Created: {directory}")

print("Directory structure created successfully!")
