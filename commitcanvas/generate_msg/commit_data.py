import pydriller
from pydriller import RepositoryMining
import os
import pandas as pd
import re

def parse_for_type(name):
    """Parse through file name and returns its format."""
    if "." in name:
        file_type, name = os.path.splitext(name)
        file_type += ""
        return name
    return name

def get_file_formats(files):
    """Create a list of unique file formats."""
    formats = []
    for file in files:
        current_format = parse_for_type(file)
        if current_format not in formats:
            formats.append(current_format)
    # sort data to ensure consistency for test
    formats = sorted(formats)
    return formats

def has_md(file_formats):
    if len(file_formats) == 1 and ".md" in file_formats:
        return True
    else:
        return False

def test_files_included(strings):
    is_test = []
    for i in strings:
        if "test" in (re.split('[^a-zA-Z]', i)):
            is_test.append(True)
        else:
            is_test.append(False)
    return is_test

def get_lined_count(diff_parsed):
    modified = 0
    added = len(diff_parsed["added"])
    deleted = len(diff_parsed["deleted"])
    for i in diff_parsed["added"]:
        for j in diff_parsed["deleted"]:
            if i[0] == j[0]:
                modified += 1
                added -= 1
                deleted -= 1
    return(added,deleted,modified)

def get_commit_data():
    commits_info = []
    commit_types = ["feat:","style:","test:","refactor:","fix:","perf:","docs:","chore:","ci:","build:"]
    for commit in RepositoryMining('https://github.com/GatorEducator/gatorgrader').traverse_commits():
        commit_type = commit.msg.lower().split()[0]
        if commit_type in commit_types:
            file_names = []
            nlocs = 0
            
            for m in commit.modifications:
                file_names.append(m.filename)
                if m.nloc is not None:
                    nlocs += m.nloc
                
            
            lines = get_lined_count(m.diff_parsed)
            commit_dict = {

                "project_name": commit.project_name,
                "commit_hash": commit.hash,
                "commit_msg": commit.msg,
                "commit_type": commit_type,
                "file_names": file_names,
                "num_files": len(file_names),
                "file_formats": get_file_formats(file_names),
                "is_test": all(test_files_included(file_names)),
                "has_md": has_md(get_file_formats(file_names)),
                "unique_file_formats": len(get_file_formats(file_names)),
                "diffs_parsed": m.diff_parsed,
                "nlocs": nlocs,
                "added": lines[0],
                "deleted": lines[1],
                "modified": lines[2],
            }
            commits_info.append(commit_dict)
            
    return commits_info

info = get_commit_data()

data = pd.DataFrame(info)
data.to_csv("data/raw_data.csv",header=True)

labels = []
for i in data["commit_type"]:
    if i in ["style:","refactor:","fix:","perf:"]:
        labels.append("modif:")
    elif i in ["chore:","build:","ci:"]:
        labels.append("chore:")
    else:
        labels.append(i)
        

print(labels)
data["commit_type"] = labels


print(data)
data.to_csv("data/training_data.csv",header=True)