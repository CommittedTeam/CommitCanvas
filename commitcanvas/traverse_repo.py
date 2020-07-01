"""Code to traverse the Git History."""
# pylint: disable=import-error
import os

from github import Github


def parse_file_type(name):
    """Parse through file name and return its format."""
    if "." in name:
        file_type, name = os.path.splitext(name)
        file_type += ""
        return name
    return name


def traverse(token, repo_name):
    """Collect the data about the commit."""
    # Get commit build status, message, file types, change types and diffs.
    data = {
        "status": [],
        "message": [],
        "file_types": [],
        "change_types": [],
        "diff": [],
    }
    githb = Github(token)

    repo = githb.get_repo(repo_name)

    commits = repo.get_commits()
    for commit in commits:

        file_type = []
        change_types = []
        diff_parsed = []

        status = commit.get_combined_status()
        data["status"].append(status.state)
        data["message"].append(commit.commit.message)
        data["file_types"].append(file_type)
        data["diff"].append(diff_parsed)
        data["change_types"].append(change_types)

        files = commit.files

        for file in files:
            change_types.append(file.status)
            diff_parsed.append(file.patch)
            # parse the filenames for the extensions
            file_type.append(parse_file_type(file.filename))

    return data
