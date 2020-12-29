import pydriller
from pydriller import RepositoryMining
import os
import pandas as pd
import re
from difflib import SequenceMatcher
from statistics import mean

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
        if "test" in (i.lower()):
            is_test.append(True)
        else:
            is_test.append(False)
    return is_test


def get_similarity_index(diffs):
    similarities = []
    for diff in diffs:
        added_lines = " ".join([x[1].strip() for x in diff["added"]])
        deleted_lines = " ".join([x[1].strip() for x in diff["deleted"]])
        similarity_ratio = SequenceMatcher(None, added_lines, deleted_lines).ratio()
        similarities.append(similarity_ratio)
    if len(similarities) > 1:
        return mean(similarities)
    else:
        return similarities[0]

def get_commit_data():
    commits_info = []
    commit_types = ["feat:","style:","test:","refactor:","docs:","chore:","ci:","build:"]
    for commit in RepositoryMining('https://github.com/GatorEducator/gatorgrader').traverse_commits():
        commit_type = commit.msg.lower().split()[0]
        
        if commit_type in commit_types:
            file_names = []
            added = 0
            removed = 0
            nlocs = 0
            diffs = []
            for m in commit.modifications:
                file_names.append(m.filename)
                if m.nloc is not None:
                    nlocs += m.nloc
                if m.added is not None:
                    added += m.added
                if m.removed is not None:
                    removed += m.removed
                diffs.append(m.diff_parsed)
                
            
                # lines = get_lined_count(m.diff_parsed)
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
                "diffs_parsed": diffs,
                "similarity": get_similarity_index(diffs),
                "nlocs": nlocs,
                "added": added,
                "removed": removed,
                "total": abs(added-removed)

            }
            commits_info.append(commit_dict)

    return commits_info


info = get_commit_data()

data = pd.DataFrame(info)
data.to_csv("data/raw_data.csv",header=True)

labels = []
for i in data["commit_type"]:
    if i in ["chore:","build:","ci:"]:
        labels.append("chore:")
    else:
        labels.append(i)
        

data["commit_type"] = labels

data.to_csv("data/training_data.csv",header=True)

# def get_lined_count(diff):
#     added = 0
#     moved = 0
#     deleted = 17
#     for diff_parsed in diff:
#         # diff_parsed dictionary value is a list of tuples, where first item is line number, and second item is line content
#         # get the second item for added and deleted
#         added_lines = [x[1] for x in diff_parsed["added"]]
#         deleted_lines = [x[1] for x in diff_parsed["deleted"]]
#         for i in added_lines:
#             # Remove extra whitespaces
#             # if added line is part of deleted line then there is high chance it was moved from the deleted line
#             if any(i.strip() in s for s in deleted_lines):
#                 moved += 1
#             else:
#                 print(i.strip())
#                 # print(SequenceMatcher(None, i.strip(), j.strip()).ratio())

                    
#     return(added,moved,deleted)
