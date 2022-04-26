"""Helper functions for entry point"""
import pluggy
from commitcanvas import hookspecs, default
from inspect import getmembers, isclass
import sys


def create_pluginmanager():
    """Create PlugginManager instance for commitcanvas.
    
    :params: None
    :return: Pluginmanager object
    """

    pm = pluggy.PluginManager("commitcanvas")
    pm.add_hookspecs(hookspecs)

    return pm


def default_tokeep(disable: str) -> list[str]:
    """Remove classes that user disabled.
    
    :params: string that has comma separated names of default plugins to be disabled
    :return: list of names of default plugins that will be kept
    """

    disable = disable.replace(" ", "").split(",")
    default_classes = getmembers(default, isclass)
    kept_default_classes = [obj for obj in default_classes if obj[0] not in disable]

    return kept_default_classes


def registrar(pm, classes: list[tuple]) -> None:
    """Register each hook
    
    :params: pm: PluginManager object
             classes: list of tuples, where each tuple has plugin's name and class
    :return: None
    """

    for obj in classes:
        pm.register(obj[1]())


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


def display_errors(errors: list[str]) -> None:
    """Print errors from checks.
    
    :params: list of strings, where each string represents the error message returned from the rule
    :return: None
    """

    if errors:
        # If there are errors from the checks display them to the user and return exit code 1
        # so that pre-commit aborts the commit
        print("\n")
        print(*errors, sep = "\n")
        sys.exit(1)

    else:
        # No errors were found so let the commit pass
        sys.exit(0)