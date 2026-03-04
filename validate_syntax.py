#!/usr/bin/env python
"""Quick syntax validation for all streamlit app Python files."""

import py_compile
import sys
from pathlib import Path

app_dir = Path("streamlit_app")
files_to_check = [
    "main.py",
    "config.py",
    "theme.py",
    "gold_analytics.py",
    "logs_observability.py",
    "data_quality.py",
    "utils/logger.py",
    "utils/cache_manager.py",
    "utils/athena_service.py",
    "utils/analytics_service.py",
    "utils/parser_service.py",
]

errors = []
for file_rel_path in files_to_check:
    file_path = app_dir / file_rel_path
    try:
        py_compile.compile(str(file_path), doraise=True)
        print(f"✓ {file_rel_path}")
    except py_compile.PyCompileError as e:
        errors.append(f"✗ {file_rel_path}: {str(e)}")
        print(f"✗ {file_rel_path}: {str(e)}")

if errors:
    print(f"\n{len(errors)} error(s) found:")
    for error in errors:
        print(f"  {error}")
    sys.exit(1)
else:
    print(f"\nAll {len(files_to_check)} files have valid syntax!")
    sys.exit(0)
