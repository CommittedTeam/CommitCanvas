"""Get commit massage from command line and do checks."""
import sys

from commitcanvas import commit_message_checker as cm

# TODO: refactor this code
def get_checks(commit_message):
    """Do all the checks for the commit message."""
    length = cm.check_length(commit_message)
    period = cm.check_for_period(commit_message)
    capital = cm.check_capital_letter(commit_message)
    blank_line = cm.check_blank_line(commit_message)
    imperative = cm.check_imperative_mood(commit_message)

    list_of_checks = [capital, blank_line, length, period, imperative]
    return list_of_checks


def commit_check(commit_message):
    """Show diagnostic info."""
    list_of_checks = get_checks(commit_message)
    # get overall boolean value, to ensure that every item
    # in the list has True value
    # and therefore all the checks pass.
    boolean_value = all(list_of_checks)
    # Display helpful tips on how to improve commit message
    if not boolean_value:
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
        # return exit code 1 if some of the checks didn't pass
        sys.exit(1)

    else:
        # all the checks passed
        sys.exit(0)
