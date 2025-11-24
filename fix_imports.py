"""Automated script to fix all imports across the codebase."""
import os
import re
from pathlib import Path


def fix_file(filepath):
    """Fix imports in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Error reading {filepath}: {e}")
        return False
    
    original = content
    
    # Define all replacements
    replacements = [
        # Fix model imports
        (r'from app\.db\.models import', 'from app.models import'),
        # Fix session/database imports
        (r'from app\.db\.session import', 'from app.database import'),
        # Fix config imports (keep core.config)
        (r'from app\.config import settings', 'from app.core.config import settings'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Check if anything changed
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[FIXED] {filepath}")
            return True
        except Exception as e:
            print(f"[ERROR] Error writing {filepath}: {e}")
            return False
    
    return False


def main():
    """Fix all Python files in app directory."""
    app_dir = Path("app")
    
    if not app_dir.exists():
        print(f"[ERROR] Directory {app_dir} not found!")
        return
    
    fixed_count = 0
    total_count = 0
    
    # Process all Python files
    for py_file in app_dir.rglob("*.py"):
        # Skip __pycache__ directories
        if "__pycache__" in str(py_file):
            continue
            
        total_count += 1
        if fix_file(py_file):
            fixed_count += 1
    
    print(f"\n[SUCCESS] Done! Fixed {fixed_count} out of {total_count} files!")
    print("\n[SUMMARY]:")
    print(f"   - from app.db.models -> from app.models")
    print(f"   - from app.db.session -> from app.database")  
    print(f"   - from app.config -> from app.core.config (settings only)")


if __name__ == "__main__":
    main()

