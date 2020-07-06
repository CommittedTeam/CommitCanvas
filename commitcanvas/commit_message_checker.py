"""Check the style of commit messages."""
# Good commit message guidelines from Github
# Separate subject from body with a blank line
# Do not end the subject line with a period
# Capitalize the subject line and each paragraph
# Use the imperative mood in the subject line
# Wrap lines at 72 characters
# Use the body to explain what and why you have done something.
# In most cases, you can leave out details about how a change has been made
# pylint: disable = import-error
import spacy


def check_blank_line(message):
    """Check if there is a blank line between subject and a paragraph."""
    splitted = message.splitlines()
    if len(splitted) > 1:
        check = not splitted[1]
    else:
        check = True

    return check


def check_for_period(message):
    """Check that there is no period in the end of the subject line."""
    splitted = message.splitlines()
    check = not splitted[0].endswith(".")

    return check


def check_length(message):
    """Length of the subject line should not be more than 72 characters."""
    splitted = message.splitlines()
    return len(splitted[0]) < 73


def check_imperative_mood(message):
    """Check if the commit message starts with a verb in imperative mood."""
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(message)

    if doc[0].tag_ != "VB":
        print("Commit message should start with verb in imperative mood")
    else:
        print("Check imperative mood....................PASSED")
    if doc[0].tag_ in ("VBD", "VBN", "VBZ", "VBG"):
        print("Try starting with", '"{}"'.format(doc[0].lemma_), "instead")


def commit_check(commit_message):
    """Display the diagnostic messages."""
    if check_blank_line(commit_message):
        print("Check for blank line.....................PASSED")
    else:
        print("Check for blank line.....................FAILED")
        print("\nBlank line required between subject and a pharagraph\n")

    if check_length(commit_message):
        print("Check for length.........................PASSED")
    else:
        print("Check for length.........................FAILED")
        print("\nThere must be less than 72 characters in the subject line\n")

    if check_for_period(commit_message):
        print("Check for period.........................PASSED")
    else:
        print("Check for period.........................FAILED")
        print("\nNo period needed at the end of the subject line\n")

    check_imperative_mood(commit_message)
