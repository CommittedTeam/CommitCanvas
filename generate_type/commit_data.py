from pydriller import RepositoryMining
import os
import pandas as pd
import re
from github import Github
import detect_type
import pathlib

def get_commit_types(commit_msg):
    """Check if commist message follows angular conventional syntax and get commit type"""
    try:
        if re.match(r'^(\w*)(?:\((.*)\))?: (.*)$',commit_msg.split('\n')[0]):      
            commit_type = re.findall( r'[a-zA-Z]+', commit_msg)[0]
            return commit_type
    except:
        return None

def parse_for_extension(paths):
    """Parse through file name and returns its extension."""
    formats = [os.path.splitext(path)[1] for path in paths]
    return formats

def get_file_extensions(file_formats):
    """Create a list of unique file extensions."""
    # get unique elements of the list using set method, list will be unordered
    unique_file_formats = list(set(parse_for_extension(file_formats)))
    # sort the set for testing purposes
    sorted_formats = sorted(unique_file_formats)
    return sorted_formats

def get_subject_line(message):
    """Separate commit subject from the commit type"""
    if message:
        subject = re.split(': |] ',message)[1]
        return subject

def isbot(commit_author_name, commit_author_email):
    """Detect bots """
    # If there is keyword bot in the author name or email then that is considered as bot
    isbot = False
    if re.findall( r'.bot.', commit_author_email) or re.findall( r'.bot.', commit_author_name):
        isbot = True
    return isbot

def test_files(paths):
    """
    Get the number of the test related files."
    """
    # This feature assumes that test files contain word "test
    test_files_count = len([path for path in paths if "test" in path.lower()])
    return test_files_count

def get_ratio(test,total):
    ratio = None
    try:
        return (test / len(total))
    except ZeroDivisionError:
        return ratio

def get_commit_data(repos):
    """Collect the commit data with pydriller."""
    commits_info = []

    for commit in RepositoryMining(repos,order="reverse").traverse_commits():
        commit_type = get_commit_types(commit.msg.lower())
        # skip commits that do not follow conventional commit types syntax
        if commit_type is not None:
            file_paths = []
            diffs = []

            commit_message = commit.msg
            author_name = commit.author.name
            author_email = commit.author.email

            for m in commit.modifications:
    
                diffs.append(m.diff)
                path = m.new_path
                # new path may return None if the file was deleted
                if path:
                    file_paths.append(path)
                else:
                    file_paths.append("deleted_file")

            file_extensions = get_file_extensions(file_paths)
            test_files_count = test_files(file_paths)

            commit_data = {

                "name": "gatorgrader",
                "language": "Python",
                "commit_hash": commit.hash,
                "commit_msg": commit_message,
                "commit_subject": get_subject_line(commit_message),
                "commit_type": commit_type,
                "commit_author_name": author_name,
                "commit_author_email": author_email,
                "isbot": isbot(author_name,author_email),               
                "file_paths": file_paths,
                "num_files": commit.files,
                "test_files": test_files_count,
                "test_files_ratio": get_ratio(test_files_count,file_paths),
                "unique_file_extensions": file_extensions,
                "num_unique_file_extensions": len(file_extensions),
                "num_lines_added": commit.insertions,
                "num_lines_removed": commit.deletions,
                "num_lines_total": commit.lines,
                "diffs": diffs,
                
            }
            commits_info.append(commit_data)


    return commits_info

def traverse_repos():
    
    # data = pd.read_csv("data/labeled_repos.csv")
    # angular = data[data.convention == "angular"]
    # angular = angular[26:50]
    commit_data = pd.DataFrame(get_commit_data("https://github.com/GatorEducator/gatorgrader"))
    commit_data = commit_data[['name', 'language', 'commit_hash', 'commit_subject', 'commit_type',
       'isbot', 'num_files', 'test_files', 'test_files_ratio',
       'unique_file_extensions', 'num_unique_file_extensions',
       'num_lines_added', 'num_lines_removed', 'num_lines_total']]
    print(commit_data)
    commit_data.to_feather("data/collect_gatorgrader.ftr")
    # commit_data.to_feather("data/collec345.ftr")

