"""Code to traverse the Git History."""
# pylint: disable=import-error
import os

import pandas as pd
from pydriller import RepositoryMining


def parse_file_type(name):
    """Parse through file name and returns its format."""
    if "." in name:
        file_type, name = os.path.splitext(name)
        file_type += ""
        return name
    return name


def traverse(path):
    """Collect the data about the commit."""
    data = {"message": [], "file_types": [], "change_types": [], "diff": []}
    for commit in RepositoryMining(path).traverse_commits():

        file_type = []
        change_types = []
        diff_parsed = []

        data["message"].append(commit.msg)
        data["file_types"].append(file_type)
        data["change_types"].append(change_types)
        data["diff"].append(diff_parsed)

        for modif in commit.modifications:
            change_types.append(modif.change_type.name)
            diff_parsed.append(modif.diff_parsed)
            file_type.append(parse_file_type(modif.filename))

    return data


PATH = "/home/teona/Documents/CommitCanvas/CommitCanvas"
print(pd.DataFrame(traverse(PATH)))
