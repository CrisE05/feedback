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
    for c in p.categories:
        print("Processing category {} ({})".format(c['id'], c['name']))
        g = p.construct_class_groups_for_category_id(c['id'])
        pickle.dump(g['all'].result, open(os.path.join(processed_categories, '{}.p'.format(c['id'])), "wb"))
        pickle.dump(g['bachelor'].result, open(os.path.join(processed_categories, '{}_bachelor.p'.format(c['id'])), "wb"))
        pickle.dump(g['master'].result, open(os.path.join(processed_categories, '{}_master.p'.format(c['id'])), "wb"))


if __name__ == "__main__":
    sys.exit(main())
