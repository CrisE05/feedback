#!/usr/bin/env python3

"""
Convert folder with JSON contents to Pickle file.
"""

import sys
import os
import json
import pickle
import argparse


def json2python(folder):
    """Load JSON files in folder as Python dictionary.
    Use filename (without the extension) as dictionary key.
    """
    data = {}
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            print("Reading {}".format(path))
            id = os.path.splitext(file)[0]
            data[id] = json.load(open(path, 'r'))
    return data


def main():
    """Convert JSON contents to Pickle file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', nargs=1, required=True,
                        help='JSON source folder')
    parser.add_argument('-d', '--destination', nargs=1, required=True,
                        help='Pickle destination file')
    args = parser.parse_args()

    data = json2python(args.source[0])
    pickle.dump(data, open(args.destination[0], 'wb'))


if __name__ == "__main__":
    sys.exit(main())
