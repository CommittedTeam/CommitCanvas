"""Feature engineering and data pre-processing."""
import pydriller
from pydriller import RepositoryMining
import os
import pandas as pd
import re
from difflib import SequenceMatcher
from statistics import mean
import matplotlib.pyplot as plt
from ast import literal_eval
import difflib


def parse_for_type(paths):
    """Parse through file name and returns its format."""
    formats = []
    for path in paths:
        # Make sure that path in collected data is not None
        if path:
            # os.path.splitext returns tuple of file name and file format. Get file format at index 1
            file_format = os.path.splitext(path)[1]
            formats.append(file_format)
    return formats


def get_file_formats(file_formats):
    """Create a list of unique file formats."""
    # get unique elements of the list using set method, list will be unordered
    unique_file_formats = list(set(parse_for_type(file_formats)))
    return unique_file_formats


def test_files_ratio(strings):
    """
    Get the ratio of the test relates files in all files modifies.
    
    This is a questionable feature because it assumes that test files contain word "test"
    """
    count = 0
    for i in strings:
        # Majority of the test related files have word "test" in the file path
        if "test" in (i.lower()):
            count += 1
    try:
        ratio = round((count / len(strings)),2)
    except ZeroDivisionError:
        ratio = None

    return ratio


def get_similarity_index(diffs):
    """
    Get similarity index between added and deleted lines.

    The current approach uses SequenceMatcher,
    However there are multiple other algorithms that may be better for finding similarity index, especially for source code
    """
    similarities = []
    # get the similarity index for each modified file separately
    for diff in diffs:
        # All the added lines per modified file will be joined
        added_lines = "\n".join([x[1] for x in diff["added"]])
        # All the deleted lines per modified file will be joined
        deleted_lines = "\n".join([x[1] for x in diff["deleted"]])
        # Similarity index will be calculated based on joined added and joined deleted lines
        similarity_ratio = SequenceMatcher(None, added_lines, deleted_lines).ratio()
        similarities.append(similarity_ratio)
    # if there are multiple files and therefore multiple similarity scores get the average
    if len(similarities) > 1:
        return mean(similarities)
    elif len(similarities) == 1:
        return similarities[0]


def get_dummies(dataframe):
    """
    Encode categorical data as dummy variables.
    
    This method is targeting encoding file extensions
    """
    # one commit may have multiple modified files and therefore multiple different file extensions
    # pandas get_dummies() can encode that as long as extensions are split by separators.
    # pandas uses "|" by default
    joined = (dataframe.str.join('|'))
    dummies = joined.str.get_dummies()

    return dummies


def add_new_features(data):
    data["total_files"] = [len(files) for files in data['file_paths']]
    data["total_lines"] = data.added - data.removed
    data['unique_file_formats'] = [get_file_formats(file_name) for file_name in data['file_paths']]
    data['similarity_index'] = [get_similarity_index(diff) for diff in data['diffs_parsed']]
    data['test_files_ratio'] = [test_files_ratio(files) for files in data['file_paths']]
    
    dummies = get_dummies(data.unique_file_formats)
    combined = pd.concat([data, dummies],axis=1)
    return combined


def drop_extra_features(data):
    features = ['project_name', 'commit_hash', 'commit_msg','file_paths', 'diffs_parsed', 'unique_file_formats']
    data = data.drop(features, axis=1)
    return data


data = pd.read_csv("data/collected_data.csv",index_col=0,converters={"file_paths": literal_eval,"diffs_parsed": literal_eval})

new_features = add_new_features(data)
# Drop rows that have nan values
new_features = new_features.dropna()

train = drop_extra_features(new_features)
print(train.columns)
train.to_csv("data/train_data.csv",header=True)


