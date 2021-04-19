"""Feature engineering and data pre-processing."""
from pydriller import RepositoryMining
import pandas as pd
from statistics import mean
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

def encode_extensions(dataframe):
    """
    Encode categorical data as dummy variables.
    
    This method is encoding file extensions
    """
    # one commit may have multiple modified files and therefore multiple different file extensions
    # pandas get_dummies() can encode that as long as extensions are split by separators.
    # pandas uses "|" by default
    extensions = dataframe["unique_file_extensions"]
    joined = (extensions.str.join('|'))
    dummies = joined.str.get_dummies()

    return dummies

def group_extensions(types,data):
    grouped_extensions = {}
    for commit_type in types:   
        new_data = data.loc[data['commit_type'] == commit_type]
        extensions = new_data["unique_file_extensions"].to_list()
        flat_list = [item for sublist in extensions for item in sublist]
        grouped_extensions.update({commit_type: flat_list})
    return grouped_extensions

def group_messages(types,data):
    """Group commit messages based on the conventional commit type they have"""
    grouped_messages = {}
    for commit_type in types:   
        new_data = data.loc[data['commit_type'] == commit_type]
        grouped_messages.update({commit_type:(new_data.commit_subject).tolist()})
    return grouped_messages

def stem_tokenizer(text):
    """Do stemming on words"""
    ps = nltk.PorterStemmer()
    tokens = [word for word in nltk.word_tokenize(text) if (word.isalpha() and word not in stopwords.words('english'))] 
    stems = [ps.stem(item) for item in tokens]
    return stems

def get_keywords(dataset,types,tokenize = None):
    """Get word frequencies for each commit type with tf-idf approach"""
    tfIdfVectorizer=TfidfVectorizer(tokenizer = tokenize )
    tfIdf = tfIdfVectorizer.fit_transform(dataset)
    keywords = {}
    for i in range(len(dataset)):
        df = pd.DataFrame(tfIdf[i].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=[types[i]])
        df = df.sort_values(types[i], ascending=False)
        df = df[(df != 0).all(1)]
        keywords.update(df.to_dict())
    return keywords

def get_keywords_for_types(data,types):

    messages = group_messages(types,data)
    dataset = [" ".join(document) for document in list(messages.values())]
    frequencies = pd.DataFrame(get_keywords(dataset,types,stem_tokenizer)).fillna(0)

    combined = []
    for subject in data.commit_subject:

        tokenized = stem_tokenizer(subject)
        # Find the frequency sums for each commit type category
        sum_ = frequencies[frequencies.index.isin(tokenized)].sum(0)
        combined.append(sum_.to_dict())

    return combined

def add_new_features():
    """ Add new features to the dataset.""" 
    data = pd.read_pickle("data/new_data.pkl")
    types = ["chore","fix","feat","refactor","test","docs"]

    dummies = encode_extensions(data)
    combined = pd.concat([data, dummies],axis=1)
    
    scores = pd.DataFrame(get_keywords_for_types(data,types))

    train_data = pd.concat([combined,scores.set_index(combined.index)],axis=1)
    train_data = train_data[train_data["commit_type"].isin(types)]
    # drop commits made by the bots
    train_data = train_data[train_data["isbot"] != True]
    # drop duplicate commits if any
    train_data = train_data.drop_duplicates("commit_hash")

    # drop features that will not be used during training
    features_drop = ["commit_hash","commit_msg","commit_subject","commit_author_name","commit_author_email","isbot","file_paths","unique_file_extensions","diffs"]
    train_data = train_data.drop(features_drop,axis=1)
    
    train_data.to_pickle("data/train_data.pkl")

add_new_features()  







