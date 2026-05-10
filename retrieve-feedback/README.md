# Retrieve Feedback

These scripts retrieve feedback from a running Moodle instance.
The connection to the Moodle instance is configured in the `moodle.conf` file.
Create the `moodle.conf` by copying the `moodle.template.conf` file and updating its contents.

The `moodlews.py` file implements functions for common functionality used by the retrieving scripts.
It uses the Moodle web service API to authenticate, list courses, list categories, dump feedbacks, dump users.
The rest of the scripts are to be called to retrieve specific information.

## Running

The typical running order is shown below:

1. Dump category information from Moodle in a Python Pickle file.
   The Pickle file stores each information about each category.
   Each course is identified by a category ID.
   In the sample run below the output Pickle file is `../../2020-2021-all/categories.p`.
   ```
   $ ./dump_categories.py -c moodle.conf -d ../../2020-2021-all/categories.p
   ```

1. Dump course information from Moodle in a Python Pickle file.
   The Pickle file stores each information about each course.
   Each course is identified by a course ID.
   In the sample run below the output Pickle file is `../../2020-2021-all/courses.p`.
   ```
   $ ./dump_courses.py -c moodle.conf -d ../../2020-2021-all/courses.p
   ```

1. Create a simple mapping of courses to categories in a Pickle file.
   Categories are hierarchical.
   A course is mapped to a category if it is part of that category or any subcategory.
   The Pickle file stores a dictionary: they key is the category ID and the value is a list of course IDs belonging (hierarchically) to that category.
   In the sample run below the output Pickle file is `../../2020-2021-all/courses4categories.p`.
   ```
   $ ./courses4categories.py -c ../../2020-2021-all/categories.p -l ../../2020-2021-all/courses.p -m ../../2020-2021-all/courses4categories.p
   ```

1. Dump feedback information from Moodle in a Python Pickle file.
   The Pickle file stores each information about each feedback.
   Each feedback is identified by a feedback ID and belongs to a course.
   In the sample run below the output Pickle file is `../../2020-2021-all/feedbacks.p`.
   ```
   $ ./dump_feedbacks.py -c moodle.conf -l ../../2020-2021-all/courses.p -d ../../2020-2021-all/feedbacks.p
   ```

1. Dump per-courses enrolled users from Moodle in Python JSON files.
   Each courses is provided a file named `<course_id>_users.json` (e.g. `2802_users.json`) with user information.
   Use a command such as
   ```
   $ mkdir ../../2020-2021-all/enrolled_users/
   $ ./dump_enrolled_users.py -c moodle.conf -l ../../2020-2021-all/courses.p -d ../../2020-2021-all/enrolled_users/
   ```

1. Dump feedback contents from Moodle in Python JSON files.
   Content for each feedback is dumped in a file named `<feedback_id>.json`.
   Feedback content in Python JSON files is stored in the current folder, using a command such as:
   ```
   $ mkdir ../../2020-2021-all/feedback_contents/
   $ ./dump_feedback_contents.py -c moodle.conf -f ../../2020-2021-all/feedbacks.p -d ../../2020-2021-all/feedback_contents/
   ```

At the end of running all the commands above, the typical contents of the output folder are:
```
$ ls -F ../../2020-2021-all/
categories.p  courses4categories.p  courses.p  enrolled_users/  feedbacks.p  feedback_contents/
```

## Others

To take a look into a Pickle file, use a command such as:
```
$ python -m pickle ../../2020-2021-all/feedbacks.p | less
```

The `json2pickle.py` file is to be used to convert JSON files in a folder in Pickle format.
It's currently unused.
