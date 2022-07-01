"""Read commit message from the file.

Check the style and return errors and respective exit code.
"""
# pylint: disable = import-error
# import os
# from inspect import getmembers
# from inspect import isclass
# from pydoc import importfile
# import pluggy
import sys
from typing import List
from typing import Optional

import typer

# from commitcanvas import hookspecs
# from commitcanvas import utils

app = typer.Typer()
FILE = ".git/COMMIT_EDITMSG"


@app.command()
def entry(
    path: Optional[List[str]] = typer.Option(None),
    commit: str = FILE,
    disable: Optional[List[str]] = typer.Option(None),
):
    """Get commit message from command line and run checks.

    All the arguments will be given by the user in THEIR
    pre-commit-config.yaml

    :params: path: optional path to the file where user added custom plugins
             commit: path to the file where commit message is stored
                    this parameter is needed for pre-commit
             disable: optional argument for the user to disable default hooks.
    :return: print error messages if any and return exit code 1

    """
    # import the python module where user defined custom plugins

    print(path)
    print(disable)
    sys.exit(1)
    # if path:
    #     user_plugins = importfile("{}/{}".format(os.getcwd(), path))
    # else:
    #     user_plugins = None

    # # remove the default plugins that user disabled
    # kept_default_classes = utils.default_tokeep(disable)

    # pluggy_manager = pluggy.PluginManager("commitcanvas")
    # pluggy_manager.add_hookspecs(hookspecs)

    # # register default plugins
    # utils.registrar(pluggy_manager, kept_default_classes)
    # # register user provided plugins
    # utils.registrar(pluggy_manager, getmembers(user_plugins, isclass))

    # errors = pluggy_manager.hook.rule(message=utils.read_message(commit))
    # utils.display_errors(errors)
