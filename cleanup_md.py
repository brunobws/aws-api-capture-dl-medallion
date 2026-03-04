#!/usr/bin/env python
"""Remove all .md files from project root."""

from pathlib import Path
import sys

root = Path(".")

md_files = [
    "ARCHITECTURE_V2.md",
    "DELIVERY_SUMMARY_V2.md",
    "DEPLOYMENT_CHECKLIST.md",
    "DOCUMENTATION_INDEX.md",
    "QUICKSTART.md",
    "QUICKSTART_DASHBOARD_V2.md",
    "README.md",
    "SETUP_GUIDE_PT.md",
    "SOLUTION_OVERVIEW.md",
    "STREAMLIT_README.md",
]

removed_count = 0
for file_name in md_files:
    file_path = root / file_name
    if file_path.exists():
        try:
            file_path.unlink()
            print(f"✓ Removed: {file_name}")
            removed_count += 1
        except Exception as e:
            print(f"✗ Error removing {file_name}: {e}")
    else:
        print(f"- Not found: {file_name}")

print(f"\nTotal removed: {removed_count}/{len(md_files)}")
