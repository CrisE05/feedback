#!/usr/bin/env python3
"""
Pack UPB structure for all faculty folders.

Usage:
    python3 pack_structure_upb.py <top-level-folder>
"""

import os
import sys
import pack_structure as ps


FACULTY_FOLDERS = [
    "01-ELECTRO",
    "02-ENERG",
    "03-ACS",
    "04-ELECTRONICA",
    "05-FIMM",
    "06-FIIR",
    "07-ISB",
    "08-Transp",
    "09-AERO",
    "10-SIM",
    "11-CHIM",
    "12-FILS",
    "13-FSA",
    "14-FIM",
    "15-FAIMA",
    "16-DPPD",
]


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <top-level-folder>", file=sys.stderr)
        sys.exit(1)

    top = sys.argv[1]

    if not os.path.isdir(top):
        print(f"Error: Argument '{top}' is not a folder.", file=sys.stderr)
        sys.exit(1)

    top = os.path.abspath(top)

    # Pack root structure
    ps.pack_structure(top)

    # Pack each faculty folder
    for faculty in FACULTY_FOLDERS:
        folder_path = os.path.join(top, faculty)
        if os.path.isdir(folder_path):
            ps.pack_structure(folder_path)

    print("Packing complete!")


if __name__ == "__main__":
    main()