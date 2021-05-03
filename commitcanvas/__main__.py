"""Command line inferface."""
# pylint: disable = import-error
import sys
from commitcanvas import commitcanvas_check
from commitcanvas.generate_type.tokenizers import stem_tokenizer
from commitcanvas.generate_type.tokenizers import dummy
from commitcanvas import get_staged_changes as gs
import joblib
import pandas as pd
import shutil
from subprocess import check_output
import io
import pkg_resources


def entry():
    """Get commit message from command line and do checks."""

    commit_msg_filepath = sys.argv[1]
    #commitcanvas_check.commit_check(commit_msg_filepath)
    stats = check_output(['git', 'diff', '--staged', "--shortstat"]).strip()
    file_names = check_output(['git', 'diff', '--staged', "--name-only"]).strip()
    
    # Figure out which branch we're on
    with open(commit_msg_filepath, 'r+') as f:
        content = f.read()
        # rewrite the file so that you avoid the seek
        f.seek(0, 0)
        stats = gs.staged_stats(stats,file_names,content)
        my_data = pkg_resources.resource_stream(__name__, "generate_type/model/trained_model.pkl")
        model = joblib.load(my_data)
        predicted = model.predict(stats)[0]
        f.write("{}: {}".format(predicted,content))


# stats = gs.staged_stats(diff, content)
# print(stats)
# def main():
#     """Get commit message from command line and do checks."""
#     # save the commit message into the file
#     shutil.copy(sys.argv[1], ".git/pre-commit-saved-commit-msg")

#     # get the commit message for the 
#     with open(".git/pre-commit-saved-commit-msg", "r") as file:
#         commit_message = file.read()

#     commitcanvas_check.commit_check(commit_message)

