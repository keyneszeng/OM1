#!/usr/bin/env python3
"""
JSON5 Config File Linter for OM1
This script validates all JSON5 configuration files in the config directory.
"""

import sys
from pathlib import Path
from typing import List, Tuple

try:
    import pyjson5
except ImportError:
    print("Error: pyjson5 is not installed. Please run: pip install pyjson5")
    sys.exit(1)


def find_json5_files(config_dir: Path) -> List[Path]:
    """Find all JSON5 files in the config directory."""
    return list(config_dir.glob("**/*.json5"))


def lint_json5_file(file_path: Path) -> Tuple[bool, str]:
    """
    Lint a single JSON5 file.
    
    Args:
        file_path: Path to the JSON5 file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Try to parse the JSON5 content
        pyjson5.loads(content)
        return True, ""
        
    except pyjson5.Json5Exception as e:
        return False, f"JSON5 parsing error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def main():
    """Main linting function."""
    # Get the config directory
    script_dir = Path(__file__).parent
    config_dir = script_dir.parent / "config"
    
    if not config_dir.exists():
        print(f"Error: Config directory not found at {config_dir}")
        sys.exit(1)
    
    # Find all JSON5 files
    json5_files = find_json5_files(config_dir)
    
    if not json5_files:
        print("No JSON5 files found in config directory")
        return
    
    print(f"Found {len(json5_files)} JSON5 file(s) to validate\n")
    
    # Lint each file
    has_errors = False
    for file_path in sorted(json5_files):
        relative_path = file_path.relative_to(config_dir.parent)
        is_valid, error_msg = lint_json5_file(file_path)
        
        if is_valid:
            print(f"✓ {relative_path}")
        else:
            print(f"✗ {relative_path}")
            print(f"  {error_msg}\n")
            has_errors = True
    
    # Exit with appropriate code
    if has_errors:
        print("\n❌ JSON5 linting failed - please fix the errors above")
        sys.exit(1)
    else:
        print(f"\n✅ All {len(json5_files)} JSON5 files are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()