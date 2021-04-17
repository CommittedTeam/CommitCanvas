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
            if (re.match(conventions[key],commit)):
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


