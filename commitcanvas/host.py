import typer
import os
from pydoc import importfile
from inspect import getmembers, isclass
from commitcanvas import utils
import pluggy
from commitcanvas import hookspecs

app = typer.Typer()

@app.command()
def entry(path: str = None, commit: str = ".git/COMMIT_EDITMSG", disable: str = ""):
    """Get commit message from command line and run checks.
    
    All the arguments will be given by the user in THEIR pre-commit-config.yaml under commitcanvas pre-commit hook specification

    :params: path: optional path to the file where user added custom plugins
             commit: path to the file where commit message is stored, this parameter is needed for pre-commit
             disable: optional argument for the user to disable default hooks.
                      The user will give string with comma separated names of plugins to disable
    :return: print error messages if any and return exit code 1 so that pre-commit aborts the commit

    """

    # import the python module where user defined custom plugins

    user_plugins = importfile('{}/{}'.format(os.getcwd(),path))

    
    # remove the default plugins that user disabled
    kept_default_classes = utils.default_tokeep(disable)

    pm = pluggy.PluginManager("commitcanvas")
    pm.add_hookspecs(hookspecs)

    # register default plugins
    utils.registrar(pm, kept_default_classes)
    # register user provided plugins
    utils.registrar(pm, getmembers(user_plugins, isclass))

    errors = pm.hook.rule(message=utils.read_message(commit))
    utils.display_errors(errors)






