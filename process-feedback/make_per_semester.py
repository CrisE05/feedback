#!/usr/bin/env python3
"""
Merge CSV files by academic series.

Usage:
    python3 make_per_series.py <csv-input-folder> <output-per-series-folder>
"""

import glob
import os
import sys


SEMESTER_SERIES = [
    "L-A1-S1",
    "L-A1-S2",
    "L-A2-S1",
    "L-A2-S2",
    "L-A3-S1",
    "L-A3-S2",
    "L-A4-S1",
    "L-A4-S2",
    "M-A1-S1",
    "M-A1-S2",
    "M-A2-S1",
    "M-A2-S2",
]

YEAR_SERIES = [
    "L-A1",
    "L-A2",
    "L-A3",
    "L-A4",
    "M-A1",
    "M-A2",
]


def merge_csv_files(csv_files, output_path):
    """
    Merge multiple CSV files into one.
    Keeps only the first header.
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

                # Write header only once
                if index == 0:
                    outfile.write(lines[0])

                # Skip header for subsequent files
                outfile.writelines(lines[1:])


def process_group(input_folder, output_folder, identifier):
    """
    Process one identifier group.
    """
    pattern = os.path.join(input_folder, f"{identifier}-*.csv")
    csv_files = sorted(glob.glob(pattern))

    if not csv_files:
        return

    output_path = os.path.join(output_folder, f"{identifier}.csv")

    merge_csv_files(csv_files, output_path)


def main():
    if len(sys.argv) != 3:
        print(
            f"Usage: {sys.argv[0]} <csv-input-folder> <output-per-series-folder>",
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

    # Semester-level aggregation
    for identifier in SEMESTER_SERIES:
        process_group(input_folder, output_folder, identifier)

    # Year-level aggregation
    for identifier in YEAR_SERIES:
        process_group(input_folder, output_folder, identifier)


if __name__ == "__main__":
    main()