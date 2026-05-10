#!/usr/bin/env python3

"""
Dump Moodle courses in Pickle format.
"""

import sys
import pickle
import argparse
import moodlews


def main():
    """Dump Moodle courses in Pickle format.
    Moodle configuration file and destination Pickle file are provided
    as arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', nargs=1, required=True,
                        help='Configuration file')
    parser.add_argument('-d', '--dump', nargs=1, required=True,
                        help='File to dump in Pickle format')
    args = parser.parse_args()

    moodlews.parse_config(args.config[0])
    moodlews.get_auth_token()
    moodlews.get_userid()
    courses = moodlews.get_courses()
    pickle.dump(courses, open(args.dump[0], "wb"))


if __name__ == "__main__":
    sys.exit(main())
