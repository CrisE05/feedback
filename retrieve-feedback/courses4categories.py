#!/usr/bin/env python3

"""
Create mapping of courses to each category.
"""

import sys
import pickle
import argparse


def courses4categories(categories, courses):
    """Map courses to categories.
    Recurse through categories and create list of courses for each
    category.
    Return is a dictionary: key is category id and value is a list
    of course ids.
    """
    mapping = {}

    for category in categories:

        recurse_categories_list = []
        for subcategory in categories:
            subcategory_paths = subcategory['path'].split('/')
            if category['id'] == 1 or str(category['id']) in subcategory_paths:
                recurse_categories_list.append(subcategory['id'])

        mapping[category['id']] = []
        for course in courses:
            if course['categoryid'] in recurse_categories_list:
                mapping[category['id']].append(course['id'])

    return mapping


def main():
    """Load categories and courses Pickle files and dump mapping in another
    Picke file.
    All three files are provided as program arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--categories', nargs=1, required=True,
                        help='Categories Pickle file (source)')
    parser.add_argument('-l', '--courses', nargs=1, required=True,
                        help='Courses Pickle file (source)')
    parser.add_argument('-m', '--mapping', nargs=1, required=True,
                        help='Courses in categories mapping (destination)')
    args = parser.parse_args()

    categories = pickle.load(open(args.categories[0], 'rb'))
    courses = pickle.load(open(args.courses[0], 'rb'))
    mapping = courses4categories(categories, courses)
    pickle.dump(mapping, open(args.mapping[0], 'wb'))


if __name__ == "__main__":
    sys.exit(main())
