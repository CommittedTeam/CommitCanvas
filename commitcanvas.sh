#!/usr/bin/env python3
import shutil
import sys
from commitcanvas import commit_message_checker

# to make this script executable run following command: chmod +x commitcanvas.sh

# save the commit message into the file
shutil.copy(sys.argv[1], '.git/pre-commit-saved-commit-msg')

# get the commit message for the commit checks
with open('.git/pre-commit-saved-commit-msg', 'r') as file:
    data = file.read()

PASSED = True

length = commit_message_checker.check_length(data)
period = commit_message_checker.check_for_period(data)
capital = commit_message_checker.check_capital_letter(data)
blank_line = commit_message_checker.check_blank_line(data)
imperative = commit_message_checker.check_imperative_mood(data)

list_of_checks = [length, period, capital, blank_line, imperative]

# get overall boolean value, to ensure that every item in the list has True value
# and therefore all the checks pass.
overall = all(list_of_checks)
# Display helpful tips on how to improve commit message

if (PASSED != overall):
    if not capital:

        print("Error: subject line should start with capital letter")

    if not blank_line:

        print("Error: blank line required between subject and a pharagraph")

    if not length:

        print("Error: keep less than 72 characters in the subject line")

    if not period:

        print("Error: no period needed at the end of the subject line")

    if not imperative:

        print("Error: start commit message with verb in imperative mood")
    exit (1)

else:
    # all the checks passed
    exit (0)
