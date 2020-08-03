"""File for collecting the training data and training Spacy language model."""
# pylint: disable = import-error
import random

import spacy
from github import Github

model = spacy.load("model")


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
def train_model(train_data):
    """Train the spacy model."""
    nlp = spacy.load("./model")

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for i in range(10):
            random.shuffle(train_data)
            for text, annotations in train_data:
                nlp.update([text], [annotations], sgd=optimizer)
    nlp.to_disk("./updated_model")


# save the collected and annotated data in file, and fix the tags based on your
# needs. Then load the data and pass it to train_model function.

# token = "798beac5e8cd6c0e8b9ea06066720254f0682a0b"
# repo = "PyCQA/pylint"
# data = collect_training_data(token,repo)
# annotated_data = annotate(data)
# import json
# #use json instead of serialization, to manually check the data
# with open('spacy_training_data/training_data.json', 'w') as file:
#     json.dump(annotated_data,file)
# import json

# with open('spacy_training_data/training_data.json', 'r') as file:
#     data_loaded  = json.load(file)
