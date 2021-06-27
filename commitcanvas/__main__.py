"""Command line inferface."""
# pyright: reportMissingImports=false
from commitcanvas_models.train_model.tokenizers import stem_tokenizer
from commitcanvas_models.train_model.tokenizers import dummy
from commitcanvas import get_staged_changes as gs
import joblib
from subprocess import check_output
import typer
import model.model as md
from commitcanvas import commitcanvas_check

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
            model = md.load()
        predicted = model.predict(stats)[0]
        f.write("{}: {}".format(predicted,content))

        commitcanvas_check.commit_check(content)