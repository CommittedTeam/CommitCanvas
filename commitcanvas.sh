#!/usr/bin/env python3
import shutil
import sys
from src import commit_message_checker
# to make this script executable run following command: chmod +x commitcanvas.sh

# save the commit message into the file, to make sure that it doesn't get lost
shutil.copy(sys.argv[1], '.git/pre-commit-saved-commit-msg')

# get the commit message for the commit checks
with open('.git/pre-commit-saved-commit-msg', 'r') as file:
    data = file.read()

PASSED = True

list_of_checks = [
        commit_message_checker.check_length(data),
        commit_message_checker.check_for_period(data),
        commit_message_checker.check_capital_letter(data),
        commit_message_checker.check_blank_line(data),
        commit_message_checker.check_imperative_mood(data) == True,
]

# get overall boolean value, to ensure that every item in the list has True value
# and therefore all the checks pass.
overall = all(list_of_checks)
# Display helpful tips on how to impro
diagnostic_info = commit_message_checker.commit_check(data)

if (PASSED != overall):
    exit (1)

else:
    exit (0)
