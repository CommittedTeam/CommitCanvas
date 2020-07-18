"""Get commit massage from command line and do checks."""
import shutil
import sys

from commitcanvas import commit_message_checker


def get_commit_message():
    """Get commit message from command line."""
    # save the commit message into the file
    shutil.copy(sys.argv[1], ".git/pre-commit-saved-commit-msg")

    # get the commit message for the commit checks
    with open(".git/pre-commit-saved-commit-msg", "r") as file:
        data = file.read()
    return data


def get_checks():
    """Do all the checks for the commit message."""
    data = get_commit_message()
    length = commit_message_checker.check_length(data)
    period = commit_message_checker.check_for_period(data)
    capital = commit_message_checker.check_capital_letter(data)
    blank_line = commit_message_checker.check_blank_line(data)
    imperative = commit_message_checker.check_imperative_mood(data)

    list_of_checks = [capital, blank_line, length, period, imperative]
    return list_of_checks


def commit_check():
    """Show diagnostic info."""
    # get overall boolean value, to ensure that every item
    # in the list has True value
    # and therefore all the checks pass.
    list_of_checks = get_checks()
    overall = all(list_of_checks)
    # Display helpful tips on how to improve commit message
    passed_default = True
    if passed_default != overall:
        if not list_of_checks[0]:

            print("Error: subject line should start with capital letter")

        if not list_of_checks[1]:

            print("Error: blank line required between subject and pharagraph")

        if not list_of_checks[2]:

            print("Error: keep less than 72 characters in the subject line")

        if not list_of_checks[3]:

            print("Error: no period needed at the end of the subject line")

        if not list_of_checks[4]:

            print("Error: start commit message with verb in imperative mood")
        sys.exit(1)

    else:
        # all the checks passed
        sys.exit(0)
