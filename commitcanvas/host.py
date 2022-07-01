"""Read commit message from the file.

Check the style and return errors and respective exit code.
"""
# pylint: disable = import-error
import os
from pydoc import importfile
from typing import List
from typing import Optional

import pluggy
import typer

from commitcanvas import hookspecs
from commitcanvas import utils

app = typer.Typer()
FILE = ".git/COMMIT_EDITMSG"


@app.command()
def entry(
    path: Optional[List[str]] = typer.Option(None),
    commit: Optional[str] = FILE,
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
    pluggy_manager = pluggy.PluginManager("commitcanvas")
    pluggy_manager.add_hookspecs(hookspecs)

    # import the python module where user defined custom plugins

    for i in path:
        plugins = importfile("{}/{}".format(os.getcwd(), i))
        kept_plugins = utils.default_tokeep(plugins, disable)
        # register user provided plugins
        utils.registrar(pluggy_manager, kept_plugins)

    errors = pluggy_manager.hook.rule(message=utils.read_message(commit))
    utils.display_errors(errors)
