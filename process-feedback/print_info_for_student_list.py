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
    parser.add_argument('-i', '--course_id', required=True,
            help='category')
    parser.add_argument('-s', '--students_list', required=True,
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
    course_students_info = []
    for cs in p.students4course(course_id=int(args.course_id)):
        if not 'customfields' in cs.keys():
            continue
        fullname = cs['fullname']
        username = cs['username']
        email = cs['email']
        anul = None
        grupa = None
        for cf in cs['customfields']:
            if cf['shortname'] == 'anul':
                year = cf['value']
            if cf['shortname'] == 'grupa':
                group = cf['value']
        course_students_info.append({
            'fullname': fullname,
            'username': username,
            'email': email,
            'year': year,
            'group': group
            })
    for s in open(args.students_list, "r").readlines():
        s = s.strip()
        for cs in course_students_info:
            if s == cs['fullname']:
                print("{},{},{},{}".format(cs['fullname'], cs['email'], cs['year'], cs['group']))


if __name__ == "__main__":
    sys.exit(main())
