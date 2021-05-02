"""Feature engineering and data pre-processing."""
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

def save():
    types = ["chore", "docs","feat","fix","refactor","test"]
    data = pd.read_feather("commitcanvas/generate_type/data/collect_gatorgrader.ftr")
    print(data.columns)
    # data = data[data.name == "serverless"]
    data = data[data["commit_type"].isin(types)]
    # drop commits made by the bots
    data = data[data["isbot"] != True]
    # drop duplicate commits if any
    data = data.drop_duplicates("commit_hash")
    #data['sub_ratio'] = data['num_lines_removed'] / data['num_lines_total']
    #data['add_ratio'] = data['num_lines_added'] / data['num_lines_total']
    # drop columns that have NAN
    data = data.dropna()
    print(data)

    # drop features that will not be used for training
    features_drop = ["name","language","commit_hash","isbot"]
    train = data.drop(features_drop,axis=1)

    # split labels and features
    label = data["commit_type"]
    train = train.drop(["commit_type"],axis=1)

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


    X_train, X_test, y_train, y_test = train_test_split(
        train, label, random_state=42)

    pipeline = pipeline.fit(X_train, y_train)
    import joblib

    print(X_test)
    predicted = pipeline.predict(X_test)

    # display classification report
    print(
    classification_report(y_test,predicted, target_names=types)
    )


    print("saving the model")
    joblib.dump(pipeline, 'commitcanvas/generate_type/model/trained_model.pkl')
    print("saving model complete")
# plot confusion matrix
# plot_confusion_matrix(pipeline, X_test, y_test, display_labels=types,cmap='Blues',normalize="true")
# plt.show()


