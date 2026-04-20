#!/usr/bin/env python3
"""
Script to create a directory structure for data processing.
Usage: python3 create_faculty_structure.py <top-level-folder>
"""

import os
import sys


def create_substructure(path):
    """
    Create a directory with subdirectories: raw, entire, per-semester.

    Args:
        path: The parent directory path
    """
    os.makedirs(os.path.join(path, "raw"), exist_ok=True)
    # os.makedirs(os.path.join(path, "common"), exist_ok=True)
    os.makedirs(os.path.join(path, "entire"), exist_ok=True)
    os.makedirs(os.path.join(path, "per-semester"), exist_ok=True)
    # os.makedirs(os.path.join(path, "per-series"), exist_ok=True)


def create_faculty_structure(top):
    create_substructure(os.path.join(top, "json"))
    create_substructure(os.path.join(top, "csv"))
    create_substructure(os.path.join(top, "processed"))
    create_substructure(os.path.join(top, "xlsx"))
    create_substructure(os.path.join(top, "processed-xlsx"))
    create_substructure(os.path.join(top, "user-json"))

    os.makedirs(os.path.join(top, "summary"), exist_ok=True)
    os.makedirs(os.path.join(top, "summary-xlsx"), exist_ok=True)

    os.makedirs(os.path.join(top, "mapping"), exist_ok=True)
    os.makedirs(os.path.join(top, "mapping", "num_feedbacks"), exist_ok=True)
    os.makedirs(os.path.join(top, "mapping", "num_users"), exist_ok=True)

    os.makedirs(os.path.join(top, "analysis"), exist_ok=True)
    os.makedirs(os.path.join(top, "analysis-xlsx"), exist_ok=True)

def main():
    """Main function to validate arguments and create directory structure."""
    # Check if exactly one argument is provided
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <top-level-folder>", file=sys.stderr)
        sys.exit(1)

    top = sys.argv[1]

    # Check if the provided argument is a valid directory
    if not os.path.isdir(top):
        print(f"Error: Argument {top} is not a folder.", file=sys.stderr)
        sys.exit(1)

    # Create substructures for various folders
    create_faculty_structure(top)


if __name__ == "__main__":
    main()
