import pydriller
from pydriller import RepositoryMining
import os
import pandas as pd
import re
from github import Github
import pygit2

def get_commit_types(commit_msg):
    commit_msg_parts = commit_msg.strip().split()          
    commit_type = re.findall( r'\w+|[^\s\w]+', commit_msg_parts[0])[0]
    # must consist of characters, to exclude emojis
    if commit_type.isalpha():
        return commit_type

def get_commit_data(repos):
    """Collect the commit data with pydriller."""
    commits_info = []
    for repo in repos:
        for commit in RepositoryMining(repo["repo_url"]).traverse_commits():

            commit_type = get_commit_types(commit.msg.lower())
            # skip commits that do not follow conventional commit types syntax
            if commit_type is not None:
                
                file_paths = []
                diffs = []

                for m in commit.modifications:
        
                    diffs.append(m.diff)
                    file_paths.append(m.new_path)
                print(repo["repo_name"])
                commit_dict = {

                    "name": repo["repo_name"],
                    "language": repo["repo_language"],
                    "url": repo["repo_url"],
                    "commit_hash": commit.hash,
                    "commit_msg": commit.msg,
                    "commit_author_name": commit.author.name,
                    "commit_author_email": commit.author.email,
                    "commit_type": commit_type,               
                    "file_paths": file_paths,
                    "diffs": diffs,
                    "num_files": commit.files,
                    "num_lines_added": commit.insertions,
                    "num_lines_removed": commit.deletions,
                    "num_lines_total": commit.lines,
                    
                }
                
                commits_info.append(commit_dict)

    return commits_info

def get_repo_data(repo_full_name):
    repo_data = []
    for name in repo_full_name:

        github = Github("token")
        repo = github.get_repo(name)
        # check that the repository is not empty and the programming language can be detected
        if repo.get_commits and repo.language is not None:
            print(name)
            data = {
                "repo_name": name,
                "repo_url": repo.clone_url,
                "repo_language": repo.language  
            }
            repo_data.append(data)

    return repo_data
