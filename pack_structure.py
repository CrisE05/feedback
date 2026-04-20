#!/usr/bin/env python3
"""
Pack UPB structure into a zip archive.

Usage:
    python3 pack_structure.py <top-level-folder>
"""

import os
import sys
import zipfile

def pack_structure(top):

    top = os.path.abspath(top)
    base = os.path.basename(top)
    parent = os.path.dirname(top)

    zip_path = os.path.join(parent, f"{base}.zip")

    folders_to_include = ["xlsx", "processed-xlsx"]
    analysis_dir = os.path.join(top, "analysis-xlsx")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:

        for folder in folders_to_include:
            abs_folder = os.path.join(top, folder)
            if os.path.isdir(abs_folder):
                for root, _, files in os.walk(abs_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, parent)
                        zf.write(file_path, arcname)

        if os.path.isdir(analysis_dir):
            for file in os.listdir(analysis_dir):
                if file.startswith("all_") and file.endswith(".xlsx"):
                    file_path = os.path.join(analysis_dir, file)
                    arcname = os.path.relpath(file_path, parent)
                    zf.write(file_path, arcname)

    print(f"Created archive: {zip_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: pack_structure.py <top>", file=sys.stderr)
        sys.exit(1)

    pack_structure(sys.argv[1])

if __name__ == "__main__":
    main()