import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt
from commitcanvas.generate_type.tokenizers import stem_tokenizer
from commitcanvas.generate_type.tokenizers import dummy
import joblib
from reporover import collect

def data_prep(url, name, language, types):
    """ Prepare data for training"""
    if url:   
        data = commit_data = collect.collect(url)
    else:
        data = pd.read_feather("commitcanvas/generate_type/data/collect_gatorgrader.ftr")
    # Select specific repository or the programming language as specified by the user
    if language is not None:
        data = data.loc[data['language'] == language]
    if name is not None:
        data = data.loc[data['name'] == name]
    
    # select commits with special types
    
    data = data[data["commit_type"].isin(types)]
    # drop commits made by the bots
    data = data[data["isbot"] != True]
    # drop duplicate commits if any
    data = data.drop_duplicates("commit_hash")
    # drop nan rows with nan values
    data = data.dropna()

    return data

        
def get_features(data):
    # list of columns that will be used for training
    features = ['commit_subject',"num_files","test_files","test_files_ratio","unique_file_extensions","num_unique_file_extensions","num_lines_added","num_lines_removed","num_lines_total"]
    train = data[features]

    return train

def get_labels(data):

    # separate commit_type coloumn as list of lables
    return data["commit_type"]


def build_pipline():

    # steps for processing the commit subject
    subject = "commit_subject"
    subject_transformer = Pipeline(steps = [('vect', CountVectorizer(tokenizer=stem_tokenizer)),
                                            ('tfidf', TfidfTransformer()),
    ])

    # steps for processing file extensions
    extension = "unique_file_extensions"
    extension_transformer = Pipeline(steps = [('vect', CountVectorizer(tokenizer=dummy,preprocessor=dummy)),
                                            ('tfidf', TfidfTransformer()),
    ])

    # create transformer steps
    t = [('subject', subject_transformer, subject),
        ('extension', extension_transformer,extension)]

    # set remainder as passthrough so that the other columns don't get lost
    col_transform = ColumnTransformer(transformers=t,remainder="passthrough")
    model = RandomForestClassifier(random_state=42)

    # set up the pipeline with transformer and model
    pipeline = Pipeline(steps=[('prep',col_transform), ('model', model)])

    return pipeline
    
# TODO cross validation needs to be tested
def train_model(url,name,language,report,save,cross):

    types = ["chore", "docs","feat","fix","refactor","test"]
    data = data_prep(url, name, language, types)

    if cross:
        train_repos = data[data["name"] != name]
        test_repo = data[data["name"] == name]
        X_train = get_features(train_repos)
        X_test = get_features(test_repo)
        
        y_train = get_labels(train_repos)
        y_test = get_labels(test_repo)
    else:
        # create a train test split
        train = get_features(data)
        label = get_labels(data)
        X_train, X_test, y_train, y_test = train_test_split(
            train, label, random_state=42)

    pipeline = build_pipline()
    pipeline = pipeline.fit(X_train, y_train)

    if save:
        print("saving the model")
        joblib.dump(pipeline, "{}/trained_model.pkl".format(path))
        print("saving model complete")

    if report:

        predicted = pipeline.predict(X_test)

        # display classification report
        print(
        classification_report(y_test,predicted, target_names=types)
        )

        plot_confusion_matrix(pipeline, X_test, y_test, display_labels=types,cmap='Blues',normalize="true")
        plt.show()

