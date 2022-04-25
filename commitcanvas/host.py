import pluggy
from commitcanvas import hookspecs,lib
from subprocess import check_output
import joblib
import typer


pm = pluggy.PluginManager("commitcanvas")
pm.add_hookspecs(hookspecs)
pm.register(lib)


app = typer.Typer()


@app.command()
def entry(path: str = None, commit: str = ".git/COMMIT_EDITMSG"):
    """Get commit message from command line and do checks."""
    commit_msg_filepath = commit
    # commitcanvas_check.commit_check(commit_msg_filepath)
    stats = check_output(["git", "diff", "--staged", "--shortstat"]).strip()
    file_names = check_output(["git", "diff", "--staged", "--name-only"]).strip()

    with open(commit_msg_filepath, "r+") as file:
        content = file.read()
        file.seek(0, 0)

        pm.hook.checkm(message=content)
        pm.hook.checkl(message=content)



