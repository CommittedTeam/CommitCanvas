"""Command line inferface."""
# pyright: reportMissingImports=false
# noqa: F401,E501
# flake8: noqa
# pylint: disable=E0401,W0611
from subprocess import check_output

import joblib
import model as md
import typer
from commitcanvas_models.train_model.tokenizers import dummy
from commitcanvas_models.train_model.tokenizers import stem_tokenizer

from commitcanvas import commitcanvas_check
from commitcanvas import get_staged_changes as gs

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
        stats = gs.staged_stats(stats, file_names, content)

        if path:
            model = joblib.load("{}/trained_model.pkl".format(path))
        else:
            model = md.load()

        predicted = model.predict(stats)[0]
        file.write("{}: {}".format(predicted, content))

        commitcanvas_check.commit_check(content)
