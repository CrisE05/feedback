#!/usr/bin/env python3

"""
Dump Moodle enrolled users in per-course JSON files.
"""

import sys
import pickle
import argparse
import moodlews


def main():
    """Dump Moodle enrolled users in per-course JSON files.
    Moodle configuration file and course Pickle file are provided
    as arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', nargs=1, required=True,
                        help='Configuration file')
    parser.add_argument('-l', '--courses', nargs=1, required=True,
                        help='Courses file in Pickle format')
    parser.add_argument('-d', '--dump', nargs=1, required=True,
                        help='Folder where to dump files')
    args = parser.parse_args()

    # Obtain Moodle credentials.
    moodlews.parse_config(args.config[0])
    moodlews.get_auth_token()
    moodlews.get_userid()

    # Retrieve courses from pickle file.
    courses = pickle.load(open(args.courses[0], "rb"))
    moodlews.dump_enrolled_users_for_courses(courses, args.dump[0])


if __name__ == "__main__":
    sys.exit(main())
