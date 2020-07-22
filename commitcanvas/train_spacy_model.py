"""File for collecting the training data and training Spacy language model."""
# pylint: disable = import-error
import random

import spacy
from github import Github

model = spacy.load("en_core_web_sm")


def collect_training_data(token, repo_name):
    """Collect commit messages from any Github repository."""
    githb = Github(token)

    repo = githb.get_repo(repo_name)

    commits = repo.get_commits()

    training_data = []
    for commit in commits:
        msg = commit.commit.message

        doc = model(msg)
        # pick the only commit messages that start with Nouns to
        # catch the verbs in imperative
        if doc[0].tag_ == "NN":
            training_data.append(msg)
    return training_data


def annotate(training_data):
    """Annotate the messages with POS."""
    tagged_data = []
    for message in training_data:
        tags = {"tags": []}
        doc = model(message)
        for i in doc:
            tags["tags"].append(i.tag_)
        tagged_data.append([message, tags])
    return tagged_data


# pylint: disable = W0612
# def train_model(training_data):
#     """Train the spacy model."""
#     n_iter = 5
#     disabled = model.disable_pipes("parser", "ner")
#     optimizer = model.begin_training()
#     for i in range(n_iter):
#         random.shuffle(training_data)
#         for text, annotations in training_data:
#             model.update([text], [annotations], sgd=optimizer)
#
#     disabled.restore()
#
#     model.to_disk("./model")


def train_model(train_data):
    """Train the spacy model."""
    nlp = spacy.load("en_core_web_sm")

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for i in range(10):
            random.shuffle(train_data)
            for text, annotations in train_data:
                nlp.update([text], [annotations], sgd=optimizer)
    nlp.to_disk("./model")


data = [["update file", {"tags": ["VB", "NN"]}]]
train_model(data)
# save the collected and annotated data in file, and fix the tags based on your
# needs. Then load the data and pass it to train_model function.


# data = collect_training_data(token,repo)
# annotated_data = annotate(data)
#
# #use json instead of serialization, to manually check the data
# with open('spacy_training_data/training_data.json', 'w') as file:
#     json.dump(annotated_data,file)

# with open('spacy_training_data/training_data.json', 'r') as file:
#     data_loaded  = json.load(file)
