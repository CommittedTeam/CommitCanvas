import pydriller
from pydriller import RepositoryMining
import os
import pandas as pd
import re
from difflib import SequenceMatcher
from statistics import mean


def get_commit_types(commit_msg):

    if ":" in commit_msg:
        type_scope = commit_msg.split(":")[0]
        if "(" in type_scope:
            return type_scope.split("(")[0]
        else:
            return type_scope

def get_commit_data(repo_url):
    """Collect the data with pydriller."""
    commits_info = []
    commit_types = ["feat","test","refactor","docs","chore","fix","perf","style","ci","build"]
    for commit in RepositoryMining('repo_url').traverse_commits():

        commit_type = get_commit_types(commit.msg.lower())
        
        if commit_type in commit_types:

            file_paths = []
            diffs = []

            added = 0
            removed = 0

            for m in commit.modifications:

                if m.added:
                    added += m.added

                if m.removed:
                    removed += m.removed
                    
                diffs.append(m.diff_parsed)
                file_paths.append(m.new_path)

            commit_dict = {

                "project_name": commit.project_name,
                "commit_hash": commit.hash,
                "commit_msg": commit.msg,
                "commit_type": commit_type,               
                "file_paths": file_paths,               
                "diffs_parsed": diffs,
                "added": added,
                "removed": removed,
                
            }
            commits_info.append(commit_dict)

    return commits_info
