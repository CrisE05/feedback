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
    parser.add_argument('-g', '--category',
            help='Directory storing data files')
    parser.add_argument('-d', '--datadir', required=True,
            help='Directory storing data files')
    parser.add_argument('-o', '--outdir', required=True,
            help='Directory storing links')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    courses = os.path.join(args.datadir, config['files']['courses'])
    categories = os.path.join(args.datadir, config['files']['categories'])
    courses4categories = os.path.join(args.datadir, config['files']['courses4categories'])
    feedbacks = os.path.join(args.datadir, config['files']['feedbacks'])
    feedback_contents = os.path.join(args.datadir, config['files']['feedback_contents'])
    users = os.path.join(args.datadir, config['files']['users'])
    #processed_courses = os.path.join(args.datadir, config['files']['processed_courses'])
    #processed_categories = os.path.join(args.datadir, config['files']['processed_categories'])

    p = processor.Processor(courses, categories, courses4categories, feedbacks, feedback_contents, users)

    courses = []
    if args.category:
        for c_id in p.courses4category(int(args.category)):
            for c in p.courses:
                if c['id'] == c_id:
                    courses.append(c)
    else:
        courses = p.courses

    for c in courses:
        print("{}: {}".format(c['shortname'], c['id']))
        short = c['shortname'].replace("/","|")
        print("Linking users id {} to name {}.".format(c['id'], short))
        try:
            os.remove(os.path.join(args.outdir, "{}.json".format(short)))
        except OSError:
            pass
        os.link(os.path.join(users, "{}.json".format(c['id'])), os.path.join(args.outdir, "{}.json".format(short)))

if __name__ == "__main__":
    sys.exit(main())
