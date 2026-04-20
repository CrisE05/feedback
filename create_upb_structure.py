#!/usr/bin/env python3
"""
Create faculty folder hierarchy.

Usage:
    python3 create_all_faculties.py <top-level-folder>
"""

import os
import sys
import create_faculty_structure as cfacs


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


def initialize_structure(folder_path):
    """
    Create faculty structure inside a folder.
    """
    try:
        cfacs.create_faculty_structure(folder_path)
    except OSError as e:
        print(
            f"Warning: Failed to create structure for {folder_path}: {e}",
            file=sys.stderr,
        )


def main():
    """
    Validate arguments and create directory hierarchy.
    """
    if len(sys.argv) != 2:
        print(
            f"Usage: {os.path.basename(sys.argv[0])} <top-level-folder>",
            file=sys.stderr,
        )
        sys.exit(1)

    top = sys.argv[1]

    if not os.path.isdir(top):
        print(f"Error: Argument '{top}' is not a folder.", file=sys.stderr)
        sys.exit(1)

    top = os.path.abspath(top)

    # Initialize top-level structure
    initialize_structure(top)

    # Create faculty folders
    for faculty in FACULTY_FOLDERS:
        faculty_path = os.path.join(top, faculty)

        try:
            os.makedirs(faculty_path, exist_ok=True)
        except OSError as e:
            print(
                f"Error: Could not create directory '{faculty_path}': {e}",
                file=sys.stderr,
            )
            continue

        initialize_structure(faculty_path)

    print("Directory structure creation complete!")


if __name__ == "__main__":
    main()