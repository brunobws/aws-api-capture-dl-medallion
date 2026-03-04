#!/usr/bin/env python3
"""
Install missing dependencies for the dashboard.
Run this if you get ModuleNotFoundError.
"""

import subprocess
import sys

packages = [
    "plotly>=5.0.0",
    "streamlit>=1.28.0",
    "pandas>=2.0.0",
    "boto3>=1.28.0",
    "pyarrow>=12.0.0",
]

print("📦 Installing missing dependencies...")
print()

for package in packages:
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print(f"✅ {package} installed")
    print()

print("=" * 60)
print("✅ All dependencies installed successfully!")
print("=" * 60)
print()
print("You can now run:")
print("  cd streamlit_app")
print("  streamlit run main.py")
print()
