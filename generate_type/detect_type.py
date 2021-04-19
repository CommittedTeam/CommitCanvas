""" Detect the conventional style.

    guidelines:

    angular: https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit
    atom: https://github.com/atom/atom/blob/master/CONTRIBUTING.md#git-commit-messages
    ember: https://github.com/emberjs/ember.js/blob/master/CONTRIBUTING.md#pull-requests
    eslint: https://eslint.org/docs/developer-guide/contributing/pull-requests
    jshint: https://github.com/jshint/jshint/blob/master/CONTRIBUTING.md#commit-message-guidelines

    NOTE: jquery commit guidelines don't mention anything about the syntax for conventioanl commit
    types. Please see https://contribute.jquery.org/commits-and-pull-requests/#commit-guidelines.
    However commit message styles in jquery repository(https://github.com/jquery/jquery) seem to be following eslint
    conventional commit styles

"""

import re
from statistics import mode
from github import Github
import time
import urllib
import calendar
import json
import pandas as pd
import giturlparse

def match(list_commits):

    # The regular expressions are adapted from https://github.com/conventional-changelog/conventional-commits-detector
    conventions = {

        "angular": r'^[a-z](\w*)(?:\((.*)\))?: (.*)$',
        "atom": r'^(:.*?:) (.*)$',
        "ember": r'^\[(.*) (.*)] (.*)$',
        "eslint": r'^[A-Z][a-z](\w*): (.*?)(?:\((.*)\))?$',
        "jshint": r'^\[\[(.*)]] (.*)$',

    }

    matches = []

    for commit in list_commits:
        temp_key = ""
        for key in conventions.keys():
            # Take only subject line from the multiline commit messages
            if (re.match(conventions[key],commit.split('\n')[0])):
                temp_key = key
                break
            else:
                temp_key = "undefined"
        matches.append(temp_key)

    return matches

def detect(matches):
    try:
        convention = mode(matches)
    except:
        convention = "undefined"
    return convention

def wait(seconds):
    print("Waiting for {} seconds ...".format(seconds))
    time.sleep(seconds)
    print("Done waiting - resume!")

def api_wait(githb):
    rl = githb.get_rate_limit()
    current_time = calendar.timegm(time.gmtime())
    if  rl.core.remaining <= 10:  # extra margin of safety
        reset_time = calendar.timegm(rl.core.reset.timetuple())
        wait(reset_time - current_time + 10.0)
    elif rl.search.remaining <= 2:
        reset_time = calendar.timegm(rl.search.reset.timetuple())
        wait(reset_time - current_time + 10.0)