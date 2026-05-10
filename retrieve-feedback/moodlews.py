#!/usr/bin/env python3

"""
Feedback-centric functions. Use Moodle web service API functions to
list courses, list feedback forms in courses and retrieve feedback contents.

Tested on UPB Moodle sites.

Configure URL and credentials in moodle.conf file.

(c) Mihai Chiroiu 18 May 2020
(c) Razvan Deaconescu, razvan.deaconescu@upb.ro
"""

import json
import requests
import sys
import os
import configparser


# Credentials used to interogate Moodle web services.
# USERNAME and BASE_URL are stored in CONFIG_FILE.
# REST_URL is derived from BASE_URL.
# MOODLE_TOKEN is the authentication token obtained via the moodle_mobile_app service.
# USERID is the user id obtained with the core_webservice_get_site_info service.
USERNAME = ""
PASSWORD = ""
BASE_URL = ""
REST_URL = ""
MOODLE_TOKEN = ""
USERID = ""


def parse_config(config_file):
    """Parse configuration file and extract Moodle URL and credentials in
    global variables.
    """
    global USERNAME
    global PASSWORD
    global BASE_URL
    global REST_URL

    config = configparser.ConfigParser()
    config.read(config_file)

    BASE_URL = config['connect']['url']
    REST_URL = BASE_URL + "/webservice/rest/server.php"
    USERNAME = config['connect']['username']
    PASSWORD = config['connect']['password']


def get_auth_token():
    """Get authentication token from login.
    The token (and user id) are required when interrogating Moodle web services.
    """
    global MOODLE_TOKEN

    token_url = BASE_URL + "/login/token.php"
    payload = {
            "username":USERNAME,
            "password":PASSWORD,
            "moodlewsrestformat":"json",
            "service":"moodle_mobile_app"
            }

    r = requests.post(token_url, params=payload)
    res_json = r.json()
    MOODLE_TOKEN = res_json['token']


def get_userid():
    """Get user id.
    The user id (and token) are required when interrogating Moodle web services.
    """
    global MOODLE_TOKEN
    global USERID

    payload = {
            "wstoken":MOODLE_TOKEN,
            "moodlewsrestformat":"json",
            "wsfunction":"core_webservice_get_site_info"
            }
    r = requests.post(REST_URL, params=payload)
    res_json = r.json()
    USERID = res_json['userid']


def get_user_courses():
    """Get coreses that current user is enrolled to.
    Use core_enrol_get_users_courses web service function.
    """
    payload = {
            "wstoken":MOODLE_TOKEN,
            "moodlewsrestformat":"json",
            "wsfunction":"core_enrol_get_users_courses",
            "userid":USERID
            }
    r = requests.post(REST_URL, params=payload)
    return r.json()


def get_courses():
    """Get all courses. This requires administrative access.
    Use core_course_get_courses web service function.
    """
    payload = {
            "wstoken":MOODLE_TOKEN,
            "moodlewsrestformat":"json",
            "wsfunction":"core_course_get_courses"
            }
    r = requests.post(REST_URL, params=payload)
    return r.json()


def get_categories():
    """Get course categories. This requires administrative access.
    Use core_course_get_categories web service function.
    """
    payload = {
            "wstoken":MOODLE_TOKEN,
            "moodlewsrestformat":"json",
            "wsfunction":"core_course_get_categories"
            }
    r = requests.post(REST_URL, params=payload)
    return r.json()


def get_enrolled_users_for_courses(courses):
    """Extract enrolled users.
    Go through courses and get enrolled users for each course.
    """
    enrolled_users = []
    for course in courses:
        payload = {
                "wstoken":MOODLE_TOKEN,
                "moodlewsrestformat":"json",
                "wsfunction":"core_enrol_get_enrolled_users",
                "courseid":int(course['id'])
                }
        r = requests.post(REST_URL, params=payload)
        res_json = r.json()
        enrolled_users.add(json.loads(res_json))
    return enrolled_users


def dump_enrolled_users_for_courses(courses, dump_folder):
    """Dump enrolled users.
    Go through courses and dump enrolled users for each course.
    """
    for course in courses:
        payload = {
                "wstoken":MOODLE_TOKEN,
                "moodlewsrestformat":"json",
                "wsfunction":"core_enrol_get_enrolled_users",
                "courseid":int(course['id'])
                }
        if course['id'] == 1:
            continue
        r = requests.post(REST_URL, params=payload)
        res_json = r.json()
        print("Dumping users for course ID: {}".format(course['id']))
        with open(os.path.join(dump_folder, str(course['id']) + ".json"), 'w') as outfile:
            json.dump(res_json, outfile)


def get_feedbacks_for_courses(courses):
    """Get list of feedbacks.
    Go through courses and get feedbacks for each course.
    In case of multiple feedback forms, get all feedbacks.
    """
    payload = {
            "wstoken":MOODLE_TOKEN,
            "moodlewsrestformat":"json",
            "wsfunction":"mod_feedbackadm_get_feedbackadms_by_courses"
            }

    # Update payload with course id information.
    # Due to limitations in querying, limit number of courses queried to
    # NUM_COURSES_PER_QUERY.
    # i is the course counter. When it reaches 50, do the query and
    # then reset it to 0.
    NUM_COURSES_PER_QUERY = 50
    i = 0

    # Use feedbacks list to store feedback information from query.
    feedbacks = []
    for course in courses:
        course_id_json = {"courseids["+str(i)+"]":course['id']}
        i += 1
        payload.update(course_id_json)

        if i == NUM_COURSES_PER_QUERY:
            r = requests.post(REST_URL, params=payload)
            res_json = r.json()
            if 'feedbackadms' in res_json.keys():
                feedbacks.extend(res_json['feedbackadms'])
            else:
                print("No feedback for {}".format(course['shortname']))
            # Reset counter.
            i = 0

    # Do one final query for remining items.
    if i > 0:
        r = requests.post(REST_URL, params=payload)
        res_json = r.json()
        if 'feedbackadms' in res_json.keys():
            feedbacks.extend(res_json['feedbackadms'])
        else:
            print("No feedback for course id {}".format(course['shortname']))

    return feedbacks


def dump_feedbacks(feedbacks, dump_folder):
    """Dump feedback contents for each feedback.
    Each feedback content is dumped in a JSON file named after the feedback id.
    """
    payload = {
            "wstoken":MOODLE_TOKEN,
            "moodlewsrestformat":"json",
            "wsfunction":"mod_feedbackadm_get_responses_analysis"
            }

    for feedback in feedbacks:
        id_json = {"feedbackadmid":feedback['id']}
        payload.update(id_json)

        r = requests.post(REST_URL, params=payload)
        res_json = r.json()
        print("Dumping feedback contents for feedback ID: {}".format(feedback['id']))
        with open(os.path.join(dump_folder, str(feedback['id'])+".json"), 'w') as outfile:
            json.dump(res_json, outfile)


def dump_feedbacks_for_courses(courses, dump_folder):
    """Dump feedback contents for feedbacks extracted from courses.
    """
    feedbacks = get_feedbacks_for_courses(courses)
    dump_feedbacks(feedbacks, dump_folder)
