import pluggy
from commitcanvas import hookspecs
import typer
import sys
import joblib



app = typer.Typer()


@app.command()
def entry(path: str = None, commit: str = ".git/COMMIT_EDITMSG"):
    """Get commit message from command line and do checks."""
    commit_msg_filepath = commit
    # commitcanvas_check.commit_check(commit_msg_filepath)

    with open(commit_msg_filepath, "r+") as file:
        content = file.read()
        file.seek(0, 0)


        pm = pluggy.PluginManager("commitcanvas")
        pm.add_hookspecs(hookspecs)
        pm.register(path)
        pm.hook.checkm(message=content)
        pm.hook.checkl(message=content)

        model = joblib.load(path)

        sys.exit(1)





