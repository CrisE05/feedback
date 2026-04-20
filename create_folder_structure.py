#!/usr/bin/env python3

import os
import sys
import subprocess
import create_faculty_structure


def main():
    # Check argument count
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <top-level-folder>", file=sys.stderr)
        sys.exit(1)

    top = sys.argv[1]

    # Check if it's a directory
    if not os.path.isdir(top):
        print(f"Error: Argument {top} is not a folder.", file=sys.stderr)
        sys.exit(1)

    # Call create_faculty_structure for the top-level folder
    # subprocess.run(["./create_faculty_structure", top])
    try:
        create_faculty_structure(top)
    except OSError:
        print("Could not initialize faculty structure.")

    # List of folders to create
    folders = [
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

    # Create each folder and call create_faculty_structure
    for folder in folders:
        folder_path = os.path.join(top, folder)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        subprocess.run(["./create_faculty_structure", folder_path])


if __name__ == "__main__":
    main()
