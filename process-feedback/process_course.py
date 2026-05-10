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
    parser.add_argument('-i', '--id', help='Course ID')
    parser.add_argument('-n', '--name', help='Course shortname')
    parser.add_argument('-d', '--datadir', required=True,
            help='Directory storing data files')
    args = parser.parse_args()

    if not args.id and not args.name:
        parser.error("At least one of -i / --id and -n / --name is required.")

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
    if args.id:
        try:
            c = next((c for c in p.courses if c['id'] == int(args.id)))
        except StopIteration:
            print("No such course (id: {})".format(args.id))
            sys.exit(1)
    elif args.name:
        try:
            c = next((c for c in p.courses if c['shortname'] == args.name))
        except StopIteration:
            print("No such course (name: {})".format(args.name))
            sys.exit(1)

    print("Processing course {} ({})".format(c['id'], c['shortname']))
    g = p.construct_group_for_course_id(c['id'])
    pickle.dump(g.result, open(os.path.join(processed_courses, '{}.p'.format(c['id'])), "wb"))


if __name__ == "__main__":
    sys.exit(main())
