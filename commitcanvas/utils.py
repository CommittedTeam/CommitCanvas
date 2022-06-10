"""Helper functions for entry point."""
import sys
from inspect import getmembers
from inspect import isclass
from typing import List

from commitcanvas import default


def default_tokeep(disable: str) -> List[str]:
    """Remove classes that user disabled.

    :params: string that has comma separated names of
            default plugins to be disabled
    :return: list of names of default plugins that will be kept
    """
    disable = disable.replace(" ", "").split(",")
    defaults = getmembers(default, isclass)
    kept_default_classes = [i for i in defaults if i[0] not in disable]

    return kept_default_classes


def registrar(pluggy_manager, classes: List[tuple]) -> None:
    """Register each hook.

    :params: pm: PluginManager object
             classes: list of tuples, where each tuple
             has plugin's name and class
    :return: None
    """
    for obj in classes:
        pluggy_manager.register(obj[1]())


def read_message(commit: str) -> str:
    """Read commit message from the file that precommit passed to commitcanvas.

    :params: path to the file that hold commit message entered by the user
    :return: the commit message
    """
    commit_msg_filepath = commit
    with open(commit_msg_filepath, "r+") as file:
        content = file.read()
        file.seek(0, 0)

        return content


def display_errors(errors: List[str]) -> None:
    """Print errors from checks.

    :params: list of strings, where each string represents the
            error message returned from the rule
    :return: None
    """
    if errors:
        # If there are errors from the checks display them to
        # the user and return exit code 1
        # so that pre-commit aborts the commit
        print("\n")
        print(*errors, sep="\n")
        sys.exit(1)

    else:
        # No errors were found so let the commit pass
        sys.exit(0)
