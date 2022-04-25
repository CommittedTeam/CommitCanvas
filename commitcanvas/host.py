import pluggy
from commitcanvas import hookspecs, default
import typer
import sys
import importlib
import os
from pydoc import importfile
from inspect import getmembers, isclass

app = typer.Typer()


@app.command()
def entry(path: str = None, commit: str = ".git/COMMIT_EDITMSG", disable: str = None):
    """Get commit message from command line and do checks."""
    commit_msg_filepath = commit

    with open(commit_msg_filepath, "r+") as file:
        content = file.read()
        file.seek(0, 0)

        pm = pluggy.PluginManager("commitcanvas")
        pm.add_hookspecs(hookspecs)
        plugins = importfile('{}/{}'.format(os.getcwd(),path))
        
        disable = disable.split(',')
        default_classes = getmembers(default, isclass)
        enabled_default_classes = [obj for obj in default_classes if obj[0] not in disable]


        for obj in enabled_default_classes:
            pm.register(obj[1]())

        classes = getmembers(plugins, isclass)
        for obj in classes:
            pm.register(obj[1]())

        errors = pm.hook.rule(message=content)
        print(errors)
        if errors:
            print("\n")
            print(*errors, sep = "\n")

            sys.exit(1)

        else:
            sys.exit(0)




