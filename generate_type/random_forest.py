import pandas as pd 
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score, cross_validate
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support

def data_prep(name, language):
    """ Prepare data for training"""
    data = pd.read_pickle("generate_type/data/train_data.pkl")
    # Select specific repository or the programming language as specified by the user
    if language is not None:
        data = data.loc[data['language'] == language]
    if name is not None:
        data = data.loc[data['name'] == name]
    
    # drop extra features
    data = data.drop("language", axis=1)
    data = data.dropna()

    return data

def get_labels(data):
    """ Encode the labels"""
    status = np.array(data["commit_type"])
    # Labels are the values we want to predict
    targetNames = np.unique(status)
    le = LabelEncoder()
    labels = le.fit_transform(status)

    return (labels, targetNames)

def get_features(data):
    """ Prepare features for training"""
    # Remove the labels from the features
    features = data.drop("commit_type", axis = 1)
    # Saving feature names for later to print feature importances list
    featureNames = list(features.columns)
    # Convert to numpy array
    features = np.array(features)

    return (features, featureNames)

def cross_project_validate(name,language):
    """ Experiment cross-project validation and return classification report for each repository"""
    data = data_prep(name,language)
    names = np.unique(np.array(data["name"]))

    cross_proj_val = []
    for name in names:

        test = data[data["name"] == name]
        train = data[data["name"] != name]

        # Prepare test split that will be one repository
        test = test.drop("name",axis=1)
        testLabels = get_labels(test)[0]
        testFeatures = get_features(test)[0]

        # Prepare train split that will be rest of repositories
        train = train.drop("name",axis=1)
        trainLabels = get_labels(train)[0]
        trainFeatures = get_features(train)[0]

        model = RandomForestClassifier(random_state=42, class_weight="balanced")

        # train the model
        model.fit(trainFeatures, trainLabels)

        scores = precision_recall_fscore_support(testLabels,model.predict(testFeatures), average='weighted', zero_division=0)

        report = {
            "name": name,
            "precision": scores[0],
            "recall": scores[1],
            "fscore": scores[2],
        }

        cross_proj_val.append(report)
    print(pd.DataFrame(cross_proj_val))


def model(name,language):
    """ Train the model and show evaluation metrics """
    data = data_prep(name,language)

    # Drop repository name as it is not needed anymore
    data = data.drop("name", axis=1)
    labels, targetNames = get_labels(data)
    features, featureNames = get_features(data)

    (trainData, testData, trainLabel, testLabel) = train_test_split(
        features, labels, test_size=0.20, stratify=labels, random_state=42
    )

    # Create the random forest model
    model = RandomForestClassifier(random_state=42, class_weight="balanced")

    # train the model
    model.fit(trainData, trainLabel)

    # print classification report
    print(
    classification_report(testLabel,model.predict(testData), target_names=targetNames)
    )

    # print feature importances
    importances = list(model.feature_importances_)
    # List of tuples with variable and importance
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(featureNames, importances)]
    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    # Print out the feature importances 
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

    # show confusion matrix
    plot_confusion_matrix(model, testData, testLabel, display_labels=targetNames,cmap='Blues',normalize="true")
    plt.show()