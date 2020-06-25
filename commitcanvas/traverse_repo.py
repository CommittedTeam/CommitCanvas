"""Code to traverse the Git History."""
# pylint: disable=import-error
import pandas as pd
from pydriller import RepositoryMining


def traverse(path):
    """Collect the data about the commit."""
    message = []
    file = []
    change_type = []
    for commit in RepositoryMining(path).traverse_commits():

        change_types = []
        file_names = []
        message.append(commit.msg)
        file.append(file_names)
        change_type.append(change_types)

        for modif in commit.modifications:
            change_types.append(modif.change_type.name)
            file_names.append(modif.filename)

        data = {"message": message, "files": file, "change_types": change_type}

    return data


PATH = "/home/teona/Documents/CommitCanvas/CommitCanvas"
print(pd.DataFrame(traverse(PATH)))
