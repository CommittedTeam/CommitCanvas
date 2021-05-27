"""Command line inferface."""
# pylint: disable = import-error
import sys
from commitcanvas import commitcanvas_check
from commitcanvas.generate_type.tokenizers import stem_tokenizer
from commitcanvas.generate_type.tokenizers import dummy
from commitcanvas import get_staged_changes as gs
import joblib
import pandas as pd
from subprocess import check_output
import io
import pkg_resources
import typer

app = typer.Typer()

@app.command()
def entry(path: str=None, commit: str=".git/COMMIT_EDITMSG"):
    """Get commit message from command line and do checks."""

    commit_msg_filepath = commit
    #commitcanvas_check.commit_check(commit_msg_filepath)
    stats = check_output(['git', 'diff', '--staged', "--shortstat"]).strip()
    file_names = check_output(['git', 'diff', '--staged', "--name-only"]).strip()
    
    with open(commit_msg_filepath, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        stats = gs.staged_stats(stats,file_names,content)

        if path:
            model = joblib.load("{}/trained_model.pkl".format(path))
        else:
            my_data = pkg_resources.resource_stream(__name__, "generate_type/model/trained_model.pkl")
            model = joblib.load(my_data)

        predicted = model.predict(stats)[0]
        f.write("{}: {}".format(predicted,content))



model = joblib.load("generate_type/model/trained_model.pkl")
print(model)
