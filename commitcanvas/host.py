import pluggy
from commitcanvas import hookspecs
import typer
import sys
import importlib
import os

app = typer.Typer()


@app.command()
def entry(pat: str = None, commit: str = ".git/COMMIT_EDITMSG"):
    """Get commit message from command line and do checks."""
    commit_msg_filepath = commit
    # commitcanvas_check.commit_check(commit_msg_filepath)

    with open(commit_msg_filepath, "r+") as file:
        content = file.read()
        file.seek(0, 0)

        pm = pluggy.PluginManager("commitcanvas")
        pm.add_hookspecs(hookspecs)

        sys.path.append(os.path.abspath(os.path.join(os.path.pardir, pat)))
        
        import os.path

        if os.path.isfile(pat):
            print ("File exist")
        else:
            print ("File not exist")
        plugins = importlib.import_module(pat)


        pm.register(plugins)

        pm.hook.checkm(message=content)
        pm.hook.checkl(message=content)

        sys.exit(1)





