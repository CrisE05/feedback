#!/usr/bin/env python3

"""
Dump Moodle metadata on feedbacks in Pickle format.
"""

import sys
import pickle
import argparse
import moodlews


def main():
    """Dump Moodle metadata on feedbacks in Pickle format.
    Moodle configuration file and destination Pickle file are provided
    as arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', nargs=1, required=True,
                        help='Configuration file')
    parser.add_argument('-l', '--courses', nargs=1, required=True,
                        help='Courses file in Pickle format')
    parser.add_argument('-d', '--dump', nargs=1, required=True,
                        help='File to dump feedbacks in Pickle format')
    args = parser.parse_args()

    # Obtain Moodle credentials.
    moodlews.parse_config(args.config[0])
    moodlews.get_auth_token()
    moodlews.get_userid()

    # Retrieve courses from pickle file.
    courses = pickle.load(open(args.courses[0], "rb"))
    feedbacks = moodlews.get_feedbacks_for_courses(courses)
    pickle.dump(feedbacks, open(args.dump[0], "wb"))


if __name__ == "__main__":
    sys.exit(main())
