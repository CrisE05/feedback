#!/usr/bin/env python3

import sys
import pathlib
import subprocess

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <data-folder> <output-folder>",file=sys.stderr)
        sys.exit(1)
    input_dir = pathlib.Path(sys.argv[1])
    output_dir = pathlib.Path(sys.argv[2])

    if not input_dir.is_dir():
        print(f"Error: Folder {input_dir} does not exist or is not a folder.", file=sys.stderr)
        sys.exit(1)

    if not output_dir.is_dir():
        print(f"Error: Folder {output_dir} does not exist or is not a folder.")
        sys.exit(1)

    category_ids = {
    "01-ELECTRO": 2,
    "02-ENERG": 3,
    "03-ACS": 4,
    "04-ELECTRONICA": 5,
    "05-FIMM": 7,
    "06-FIIR": 8,
    "07-ISB": 9,
    "08-Transp": 10,
    "09-AERO": 11,
    "10-SIM": 12,
    "11-CHIM": 13,
    "12-FILS": 14,
    "13-FSA": 15,
    "14-FIM": 16,
    "15-FAIMA": 17,
    "16-DPPD": 18
    }

    for faculty, id in category_ids.items():

        user_json = output_dir / faculty / "user-json" / "raw"
        raw_json = output_dir / faculty / "json" / "raw"
        try:
            subprocess.run(
                ["./link_users.py",
                "-g", str(id),
                "-d", str(input_dir),
                "-o", str(user_json)],
                check=True)
        except subprocess.CalledProcessError as e:
            print(f"link_user failed for {faculty} with error {e}")
        try:
            subprocess.run(
                ["./link_feedbacks.py",
                "-g", str(id),
                "-d", str(input_dir),
                "-o", str(raw_json)],
                check=True)
        except subprocess.CalledProcessError as e:
            print(f"link_feedback failed for {faculty} with error {e}")

if __name__ == "__main__":
    main()