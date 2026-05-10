#!/usr/bin/env python

import sys
import csv


def main():
    if len(sys.argv) != 4:
        sys.stderr.write("Usage: {} <raw-feedback-csv-file> <num-user-csv-file> <prof-courses-csv-file>\n".format(sys.argv[0]))
        sys.exit(1)

    num_users = {}
    csvfile = open(sys.argv[2], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        num_users[row[0]] = int(row[1])
    csvfile.close()

    prof_courses = {}
    csvfile = open(sys.argv[3], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        prof_courses[row[0]] = row[1]
    csvfile.close()

    res = {}
    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        course = row[0]
        num = int(row[1])
        val = float(row[2])
        if not course in num_users.keys():
            sys.stderr.write("Error: Course {} absent.\n".format(course))
            sys.exit(1)
        if num_users[course] == 0:
            continue
        perc = (100.0 * num) / num_users[course]
        res[course] = {
                "prof": prof_courses[course],
                "num": num,
                "users": num_users[course],
                "perc": perc,
                "val": val
                }
    csvfile.close()

    for course in res:
        print("\"{}\",\"{}\",\"{:d}\",\"{:4.2f}\",\"{:d}\",\"{:3.2f}\"".format(course, res[course]["prof"], res[course]["num"], res[course]["perc"], res[course]["users"], res[course]["val"]))


if __name__ == "__main__":
    sys.exit(main())
