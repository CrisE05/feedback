#!/usr/bin/env python3

"""
Dump Moodle feedback contents in per-feedback JSON files.
"""

import sys
import pickle
import argparse
import moodlews


def main():
    """Dump Moodle feedback contents in per-feedback JSON files.
    Moodle configuration file and feedback metadata Pickle file are provided
    as arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', nargs=1, required=True,
                        help='Configuration file')
    parser.add_argument('-f', '--feedbacks', nargs=1, required=True,
                        help='Feedbacks file in Pickle format')
    parser.add_argument('-d', '--dump', nargs=1, required=True,
                        help='Folder where to dumpe files')
    args = parser.parse_args()

    # Obtain Moodle credentials.
    moodlews.parse_config(args.config[0])
    moodlews.get_auth_token()
    moodlews.get_userid()

    # Retrieve feedbacks from pickle file.
    feedbacks = pickle.load(open(args.feedbacks[0], "rb"))
    moodlews.dump_feedbacks(feedbacks, args.dump[0])


if __name__ == "__main__":
    sys.exit(main())
