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


def check_imperative_mood(message):
    """Check if the commit message starts with a verb in imperative mood."""
    # path = pathlib.Path(__file__).parent / "model"
    message = message.lower()
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(message)
    # NOTE: this part will be modified
    return doc[0].tag_ in ["VB", "VBP", "NNP"] or doc[0].dep_ == "compound"
