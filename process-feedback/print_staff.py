#!/usr/bin/env python

import sys
import os
import argparse
import configparser
import pickle
import processor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
            default='processor.conf', help='Configuration file (default processor.conf)')
    parser.add_argument('-g', '--category', required=True,
            help='category')
    parser.add_argument('-d', '--datadir', required=True,
            help='Directory storing data files')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    courses = os.path.join(args.datadir, config['files']['courses'])
    categories = os.path.join(args.datadir, config['files']['categories'])
    courses4categories = os.path.join(args.datadir, config['files']['courses4categories'])
    feedbacks = os.path.join(args.datadir, config['files']['feedbacks'])
    feedback_contents = os.path.join(args.datadir, config['files']['feedback_contents'])
    users = os.path.join(args.datadir, config['files']['users'])
    processed_courses = os.path.join(args.datadir, config['files']['processed_courses'])
    processed_categories = os.path.join(args.datadir, config['files']['processed_categories'])

    p = processor.Processor(courses, categories, courses4categories, feedbacks, feedback_contents, users)
    print("\"{}\";\"{}\";\"{}\";\"{}\"".format("Shortname", "Fullname", "Titulari curs", "Titulari aplicații"))
    for c_id in p.courses4category(int(args.category)):
        c = next((course for course in p.courses if course['id'] == c_id))
        if not c:
            continue
        msg = "\"{}\";\"{}\";\"".format(c['shortname'], c['fullname'])
        for prof in p.profs4course(course_id=c['id']):
            msg += "{} <{}>, ".format(prof['fullname'], prof['email'])
        msg += "\";\""
        for prof in p.assists4course(course_id=c['id']):
            msg += "{} <{}>, ".format(prof['fullname'], prof['email'])
        msg += "\""
        print(msg)


if __name__ == "__main__":
    sys.exit(main())
