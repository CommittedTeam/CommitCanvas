import typer
import os
from pydoc import importfile
from inspect import getmembers, isclass
from commitcanvas import utils

app = typer.Typer()

@app.command()
def entry(path: str = None, commit: str = ".git/COMMIT_EDITMSG", disable: str = ""):
    """Get commit message from command line and run checks.
    
    All the arguments will be given by the user in THEIR pre-commit-config.yaml under commitcanvas pre-commit hook specification

    :params: path: optional path to the file where user added custom plugins
             commit: path to the file where commit message is stored, this parameter is needed for pre-commit
             disable: optional argument for the user to disable default hooks.
                      The user will give string with comma separated names of plugins to disable
    :return: print error messages if any and return exit code 1 for the commit to be aborted by pre-commit

    """


    user_plugins = importfile('{}/{}'.format(os.getcwd(),path))
    
    kept_default_classes = utils.default_tokeep(disable)

    pm = utils.create_pluginmanager()

    utils.registrar(pm, kept_default_classes)

    utils.registrar(pm, getmembers(user_plugins, isclass))

    errors = pm.hook.rule(message=utils.read_message(commit))

    utils.display_errors(errors)






