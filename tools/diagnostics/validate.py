#!/usr/bin/env python3
"""
HUF Document Validator
Validates .docx files for structural integrity and basic content checks.
Usage: python validate.py <path_to_docx>
"""

import sys
import os
import zipfile


def validate_docx(filepath):
    """Validate a .docx file for basic structural integrity."""
    errors = []
    warnings = []

    # Check file exists
    if not os.path.exists(filepath):
        print(f"FAIL: File not found: {filepath}")
        return False

    # Check extension
    if not filepath.lower().endswith('.docx'):
        print(f"FAIL: Not a .docx file: {filepath}")
        return False

    # Check file size
    size = os.path.getsize(filepath)
    if size == 0:
        print(f"FAIL: Empty file: {filepath}")
        return False

    # Check it's a valid ZIP (docx is a ZIP archive)
    if not zipfile.is_zipfile(filepath):
        print(f"FAIL: Not a valid ZIP/DOCX archive: {filepath}")
        return False

    # Open and inspect contents
    try:
        with zipfile.ZipFile(filepath, 'r') as zf:
            names = zf.namelist()

            # Required parts of a valid .docx
            required = ['[Content_Types].xml', 'word/document.xml']
            for req in required:
                if req not in names:
                    errors.append(f"Missing required part: {req}")

            # Check for corruption
            bad = zf.testzip()
            if bad is not None:
                errors.append(f"Corrupt entry in archive: {bad}")

            # Count paragraphs in document.xml
            if 'word/document.xml' in names:
                content = zf.read('word/document.xml').decode('utf-8', errors='replace')
                para_count = content.count('<w:p ')
                if para_count == 0:
                    para_count = content.count('<w:p>')
                if para_count == 0:
                    warnings.append("No paragraphs found in document.xml")

            # Report
            file_kb = size / 1024
            part_count = len(names)

    except zipfile.BadZipFile:
        print(f"FAIL: Corrupt ZIP archive: {filepath}")
        return False
    except Exception as e:
        print(f"FAIL: Error reading {filepath}: {e}")
        return False

    # Output results
    basename = os.path.basename(filepath)
    if errors:
        print(f"FAIL: {basename}")
        for e in errors:
            print(f"  ERROR: {e}")
        return False
    else:
        print(f"OK: {basename} ({file_kb:.1f} KB, {part_count} parts, ~{para_count} paragraphs)")
        for w in warnings:
            print(f"  WARN: {w}")
        return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <file.docx> [file2.docx ...]")
        sys.exit(1)

    all_ok = True
    for filepath in sys.argv[1:]:
        if not validate_docx(filepath):
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()
