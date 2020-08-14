"""Command line inferface."""
# pylint: disable = import-error
import shutil
import sys

from commitcanvas import commitcanvas_check


def main():
    """Get commit message from command line and do checks."""
    # save the commit message into the file
    shutil.copy(sys.argv[1], ".git/pre-commit-saved-commit-msg")

    # get the commit message for the commit checks
    with open(".git/pre-commit-saved-commit-msg", "r") as file:
        commit_message = file.read()

    commitcanvas_check.commit_check(commit_message)


if __name__ == "__main__":
    main()
