# """Training and evaluating the classification model."""
# import typer
# from typing import Tuple
# from generate_type import random_forest as rf

# app = typer.Typer()

# @app.callback()
# def callback():
#     """
#     classify command takes three arguments, please see the documentation for more details
#     """

# @app.command()
# def classify(name: str = None, language: str = None, cross: bool = False):
#     """
#     random forest model with specified data
#     """
#     if ((language and name) is not None):      
#         raise typer.BadParameter("If value for language is not empty, value for name must be empty")
#     if cross:
#         if name is not None:
#             raise typer.BadParameter("If value for cross is True, value for name must be empty")
#         else:
#             rf.cross_project_validate(name,language)
#     else:
#         rf.model(name,language)

import sys
from commitcanvas.generate_type.tokenizers import stem_tokenizer
from commitcanvas.generate_type.tokenizers import dummy
from commitcanvas.generate_type import commit_data as cm
import joblib
import pandas as pd
import shutil
from subprocess import check_output
import io
import pkg_resources

def staged_stats(diff,commit_subject):

    decoded_diff = diff.decode('utf-8')

    # convert to string output into pandas dataframe for easier calculations
    data = io.StringIO(decoded_diff)
    df = pd.read_csv(data, sep="\t",names = ["added","deleted","file_paths"])


    added = df.added.sum()
    deleted = df.deleted.sum()
    paths = df.file_paths.tolist()
    file_extensions = cm.get_file_extensions(paths)
    test_files_count = cm.test_files(paths)


    staged_changes_stats = {
        'commit_subject': commit_subject,
        "num_files": len(paths),
        "test_files": test_files_count,
        "test_files_ratio": cm.get_ratio(test_files_count,paths),
        "unique_file_extensions": file_extensions,
        "num_unique_file_extensions": len(file_extensions),
        "num_lines_added": added,
        "num_lines_removed": deleted,
        "num_lines_total": added + deleted,    
    }

    return (pd.DataFrame([staged_changes_stats]))



def entry():
    """Get commit message from command line and do checks."""

    commit_msg_filepath = sys.argv[1]
    #commitcanvas_check.commit_check(commit_msg_filepath)
    diff = check_output(['git', 'diff', '--staged','--numstat']).strip()
    
    # Figure out which branch we're on
    with open(commit_msg_filepath, 'r+') as f:
        content = f.read()
        # rewrite the file so that you avoid the seek
        f.seek(0, 0)
        stats = staged_stats(diff, content)
        my_data = pkg_resources.resource_stream(__name__, "model/trained_model.pkl")
        model = joblib.load(my_data)
        predicted = model.predict(stats)[0]
        f.write("{}: {}".format(predicted,content))

# def entry():
#     stats = {
#             'commit_subject': "update revision id",
#             "num_files": 1,
#             "test_files": 0,
#             "test_files_ratio": 0.0,
#             "unique_file_extensions": [".yaml"],
#             "num_unique_file_extensions": 1,
#             "num_lines_added": 1,
#             "num_lines_removed": 1,
#             "num_lines_total": 2, 
#     }

#     diff = (pd.DataFrame([stats]))
#     my_data = pkg_resources.resource_stream(__name__, "model/trained_model.pkl")
#     print(my_data)
#     model = joblib.load(my_data)
#     predicted = model.predict(diff)
#     print(predicted)