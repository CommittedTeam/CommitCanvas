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
import jellyfish
import datetime
import statistics
from cdifflib import CSequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import itertools
import numba
import numpy as np

def parse_for_type(paths):
    """Parse through file name and returns its extension."""
    formats = []
    for path in paths:
        # Make sure that path in collected data is not None
        if path:
            # os.path.splitext returns tuple of file name and file format. Get file format at index 1
            file_format = os.path.splitext(path)[1]
            formats.append(file_format)
    return formats


def get_file_formats(file_formats):
    """Create a list of unique file extensions."""
    # get unique elements of the list using set method, list will be unordered
    unique_file_formats = list(set(parse_for_type(file_formats)))
    # sort the set for testing purposes
    sorted_formats = sorted(unique_file_formats)
    return sorted_formats

def test_files_ratio(strings):
    """
    Get the ratio of the test related files in all files modified.
    
    This feature assumes that test files contain word "test"
    """
    count = 0
    for i in strings:
        # Majority of the test related files have word "test" in the file path
        if i:
            if "test" in (i.lower()):
                count += 1
    try:
        ratio = round((count / len(strings)),2)
    except ZeroDivisionError:
        ratio = None

    return ratio

def get_dummies(dataframe):
    """
    Encode categorical data as dummy variables.
    
    This method is encoding file extensions
    """
    # one commit may have multiple modified files and therefore multiple different file extensions
    # pandas get_dummies() can encode that as long as extensions are split by separators.
    # pandas uses "|" by default
    joined = (dataframe.str.join('|'))
    dummies = joined.str.get_dummies()

    return dummies

def get_churns(diff):
    """ get code churns from the diff """
    churns = []
    diff = diff.splitlines()
    diff.append("\n")
    i = 0
    while(i < len(diff)):              
        tmp = []
        while ((diff[i].startswith('+') or diff[i].startswith('-'))) :
            tmp.append(diff[i])
            i += 1
        if tmp: 
            churns.append(tmp)
        i += 1 
    return churns

def filter_churns(churn):
    """ Classify the code churn into added and deleted """
    churns = {
        "added" : [],
        "deleted": []
    }
    for i in churn:
        if i.startswith("-"):
            churns["deleted"].append(i[1:])
        else:
            churns["added"].append(i[1:])
    return churns

def get_style_churns(churns):
    """Count how many of the code churns were non functional changes such as whitespace, blank line, punctuaions"""
    non_alum = 0
    for churn in churns:
        filtered = filter_churns(churn)
        deleted = "".join(filtered["deleted"])
        added = "".join(filtered["added"])
        set1 = set(deleted) 
        set2 = set(added) 
        common = list(set1 & set2) 
        # NOTE Needs to be refactored
        result = [ch for ch in deleted if ch not in common] + [ch for ch in added if ch not in common]
        if not result or re.match(r'^[_\W]+$',"".join(result)):       
            non_alum += 1
    if churns:
        return non_alum/len(churns)

def detect_bots(row):
    """ If there is keyword: bot in the author name or email then that is considered as bot"""
    if re.findall( r'.bot.', row["commit_author_email"]) or re.findall( r'.bot.', row["commit_author_name"]):
        return True

def get_subject_line(message):
    """Separate commit subject from the commit type"""
    return (message.split(":")[1].strip())

def group_messages(types,data):
    """Group commit messages based on the conventional commit type they have"""
    parsed_messages = {}
    for commit_type in types:   
        new_data = data.loc[data['commit_type'] == commit_type]
        parsed_messages.update({commit_type:(new_data.commit_subject).tolist()})
    return parsed_messages

def stem_tokenizer(text):
    """Do stemming on words"""
    ps = PorterStemmer()
    tokens = [word for word in nltk.word_tokenize(text) if (word.isalpha() and word not in stopwords.words('english'))] 
    stems = [ps.stem(item) for item in tokens]
    return stems

def get_keywords(dataset,types):
    """Get word frequencies for each commit type with tf-idf approach"""
    tfIdfVectorizer=TfidfVectorizer(tokenizer = stem_tokenizer)
    tfIdf = tfIdfVectorizer.fit_transform(dataset)
    keywords = {}
    for i in range(len(dataset)):
        df = pd.DataFrame(tfIdf[i].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=[types[i]])
        df = df.sort_values(types[i], ascending=False)
        df = df[(df != 0).all(1)]
        keywords.update(df.to_dict())
    return(keywords)

def get_keywords_for_data(types,data):
    """Count the frequencey of keywords in the commit message for each conventional commit type"""
    subjects = data.commit_subject.tolist()
    tokenized = [stem_tokenizer(subject) for subject in subjects]

    messages = group_messages(types,data)
    dataset = [" ".join(document) for document in list(messages.values())]
    words = (get_keywords(dataset,types))

    combined = []
    for i in tokenized:
        dictionary = {"chore": 0, "ci": 0,"build": 0, "fix": 0,"feat": 0,"docs": 0,"refactor": 0,"test": 0,"style": 0}
        for token in i:
            for key, value in words.items():
                for keyword in list(value.keys()):
                    if token == keyword:
                        dictionary[key] += value[keyword]
        combined.append(dictionary)
    return(pd.DataFrame(combined))

# NOTE needs to be refactored because according to pandas documentation apply function is very slow and there are other better ways for implementing this
def add_new_features(types,data):
    """ Add new features to the dataset."""
    data["commit_subject"]= data['commit_msg'].apply(lambda message: get_subject_line(message))
    data["churns"] = data['diffs'].apply(lambda diff: get_churns("".join(diff)))
    data["churns_count"] = data['churns'].apply(lambda diff: len(diff))
    data["style_churns"] = data['churns'].apply(lambda diff: get_style_churns(diff))
    data["commit_subject"]= data['commit_msg'].apply(lambda message: get_subject_line(message))
    data["test_files_ratio"] = data['file_paths'].apply(lambda files: test_files_ratio(files))
    data["unique_file_formats"] = data['file_paths'].apply(lambda files: get_file_formats(files))
    data["num_unique_extensions"] = data['unique_file_formats'].apply(lambda files: len(files))
    
    keywords_for_data = (get_keywords_for_data(types,data))

    dummies = get_dummies(data.unique_file_formats)
    combined = pd.concat([data, dummies],axis=1)

    train_data = pd.concat([combined,keywords_for_data.set_index(combined.index)],axis=1)

    train_data.to_pickle("data/train_data.pkl")

    return combined




