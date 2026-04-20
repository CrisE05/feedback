#!/usr/bin/env python3
"""
Merge CSV files by identifier.

Usage:
    python3 merge_common_csv.py <csv-input-folder> <output-common-folder>
"""

import os
import re
import sys
import glob


PATTERN = re.compile(r"[LM]-A[1-4]-S[1-2]-[^-]+")


def extract_ids(input_folder):
    """
    Extract unique IDs from CSV filenames.
    """
    ids = set()

    for path in glob.glob(os.path.join(input_folder, "*.csv")):
        basename = os.path.basename(path)

        match = PATTERN.search(basename)
        if match:
            ids.add(match.group(0))

    return sorted(ids)


def merge_csv_group(csv_files, output_path):
    """
    Merge CSV files into a single output file.
    Keeps the header only once.
    """
    if not csv_files:
        return

    print(f"Creating {output_path} ...")

    with open(output_path, "w", encoding="utf-8") as outfile:
        for index, csv_file in enumerate(csv_files):
            with open(csv_file, "r", encoding="utf-8") as infile:
                lines = infile.readlines()

                if not lines:
                    continue

                # Write header only from first file
                if index == 0:
                    outfile.write(lines[0])

                # Skip header for all files
                outfile.writelines(lines[1:])


def main():
    if len(sys.argv) != 3:
        print(
            f"Usage: {sys.argv[0]} <csv-input-folder> <output-common-folder>",
            file=sys.stderr,
        )
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    if not os.path.isdir(input_folder):
        print(
            f"Error: Folder '{input_folder}' does not exist or is not a folder.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not os.path.isdir(output_folder):
        print(
            f"Error: Folder '{output_folder}' does not exist or is not a folder.",
            file=sys.stderr,
        )
        sys.exit(1)

    ids = extract_ids(input_folder)

    for identifier in ids:
        pattern = os.path.join(input_folder, f"{identifier}-*.csv")
        csv_files = sorted(glob.glob(pattern))

        num = len(csv_files)

        if num == 0:
            continue

        if num == 1:
            output_name = os.path.basename(csv_files[0])
        else:
            output_name = f"{identifier}-all.csv"

        output_path = os.path.join(output_folder, output_name)

        merge_csv_group(csv_files, output_path)


if __name__ == "__main__":
    main()