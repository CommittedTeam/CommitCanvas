"""Code to traverse the Git History."""
# pylint: disable=import-error
import os

from github import Github
from pydriller import RepositoryMining


def parse_file_type(name):
    """Parse through file name and returns its format."""
    if "." in name:
        file_type, name = os.path.splitext(name)
        file_type += ""
        return name
    return name


def traverse(path, token, repo_name):
    """Collect the data about the commit."""
    # Get commit message, file types, change types and diffs with Pydriller.
    # diff: dictionary with two keys Added and Deleted, that contain list of
    # added and deleted lines.
    data = {
        "status": [],
        "message": [],
        "file_types": [],
        "change_types": [],
        "diff": [],
    }
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
            # parse the filenames for the extensions
            file_type.append(parse_file_type(modif.filename))

    # Get the build statuses for invividual commits using PyGithub
    githb = Github(token)

    repo = githb.get_repo(repo_name)

    commits = repo.get_commits()
    for commit in commits:

        status = commit.get_combined_status()
        data["status"].append(status.state)

    return data
