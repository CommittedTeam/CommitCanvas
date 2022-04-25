import typer
import sys
import os
from pydoc import importfile
from inspect import getmembers, isclass
from commitcanvas import utils

app = typer.Typer()


@app.command()
def entry(path: str = None, commit: str = ".git/COMMIT_EDITMSG", disable: str = ""):
    """Get commit message from command line and do checks."""


    user_plugins = importfile('{}/{}'.format(os.getcwd(),path))
    
    kept_default_classes = utils.default_tokeep(disable)

    pm = utils.create_pluginmanager()

    utils.registrar(pm, kept_default_classes)

    utils.registrar(pm, getmembers(user_plugins, isclass))

    errors = pm.hook.rule(message=utils.read_message(commit))

    if errors:
        print("\n")
        print(*errors, sep = "\n")

        sys.exit(1)

    else:
        sys.exit(0)




