"""Check the style of commit messages."""
# Guidelines:
# Separate subject from body with a blank line
# Do not end the subject line with a period
# Capitalize the subject line and each paragraph
# Use the imperative mood in the subject line
# Wrap lines at 72 characters
# Use the body to explain what and why you have done something
# In most cases, you can leave out details about how a change has been mad
# pylint: disable = import-error
import spacy


def check_blank_line(message):
    """Check if there is a blank line between subject and a paragraph."""
    splitted = message.splitlines()
    if len(splitted) > 1:
        # check should only be needed for multyline commit messages
        check = not splitted[1]
    else:
        check = True

    return check


def check_for_period(message):
    """Check that there is no period in the end of the subject line."""
    splitted = message.splitlines()
    check = not splitted[0].endswith(".")

    return check


def check_capital_letter(message):
    """Check that subject line starts with capital letter."""
    check = message[0].isupper()

    return check


def check_length(message):
    """Length of the subject line should not be more than 72 characters."""
    splitted = message.splitlines()
    return len(splitted[0]) < 73


# disable pylint no-else-return error
# pylint: disable = R1705
def check_imperative_mood(message):
    """Check if the commit message starts with a verb in imperative mood."""
    model = spacy.load("./model")

    doc = model(message)

    if doc[0].tag_ != "VB":
        return (False, "Start message with verb in imperative mood")
    else:
        return True


FAIL = "\u2715"
PASS = "\u2713"


def commit_check(commit_message):
    """Display the diagnostic messages."""
    if check_capital_letter(commit_message):

        print(PASS, " Check for capital letter")
    else:

        print(FAIL, " Check for capital letter")
        print("\nSubject line should start with capital letter\n")

    if check_blank_line(commit_message):
        print(PASS, " Check for blank line")
    else:
        print(FAIL, " Check for blank line")
        print("\nBlank line required between subject and a pharagraph\n")

    if check_length(commit_message):
        print(PASS, " Check for length")
    else:
        print(FAIL, " Check for length")
        print("\nThere must be less than 72 characters in the subject line\n")

    if check_for_period(commit_message):
        print(PASS, " Check for period")
    else:
        print(FAIL, " Check for period")
        print("\nNo period needed at the end of the subject line\n")

    if check_imperative_mood(commit_message) is True:
        print(PASS, " Check for imperative mood")
    elif check_imperative_mood(commit_message)[0] is False:
        print(FAIL, " Check for imperative mood failed\n")
        print(check_imperative_mood(commit_message)[1])
