"""Training and evaluating the classification model."""
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score, cross_validate
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

def label_encoding(data):
    # encode the labels
    target = data["commit_type"]
    status = np.array(target)
    # Labels are the values we want to predict

    targetNames = np.unique(status)
    le = LabelEncoder()
    labels = le.fit_transform(status)

    return (labels,targetNames)

def get_features(data):
    # Remove the labels from the features
    features = data.drop("commit_type", axis = 1)

    # Saving feature names for later to print feature importances list
    featureNames = list(features.columns)
    # Convert to numpy array
    features = np.array(features)

    return (features,featureNames)

def train_model():
    model.fit(trainData, trainLabel)

def cross_validation_scores():
    skf = StratifiedKFold(n_splits=5)
    scores_metrics = ["recall_weighted","precision_weighted","f1_weighted"]
    
    scores = cross_validate(model,trainData,trainLabel, scoring = scores_metrics,  cv=skf, return_train_score = True)
    all_scores = []
    for i in scores_metrics:
        test_formated = "test_{}".format(i)
        train_formated = "train_{}".format(i)
        test = scores[test_formated]
        test_mean = round(test.mean(),2)
        test_std = round(test.std(),2)
        train = scores[train_formated]
        train_mean = round(train.mean(),2)
        train_std = round(train.std(),2)

        scoring = {

            "metric": i,
            "test_mean": test_mean,
            "test_std": test_std,
            "train_mean": train_mean,
            "train_std": train_std,
        }

        all_scores.append(scoring)
    return all_scores

def print_feature_importances():
    importances = list(model.feature_importances_)
    # List of tuples with variable and importance
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(featureNames, importances)]
    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    # Print out the feature and importances 
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

# read the training data and split it into features and labels
data = pd.read_csv("data/train_data.csv",index_col=0)

labels = label_encoding(data)[0]
targetNames = label_encoding(data)[1]

features = get_features(data)[0]
featureNames = get_features(data)[1]

# construct the training and testing splits
(trainData, testData, trainLabel, testLabel) = train_test_split(
    features, labels, test_size=0.10, stratify=labels, random_state=42
)

# Create the random forest model
model = RandomForestClassifier(random_state=42, class_weight="balanced", max_depth=13)

# display stratified 5 fold cross validation scores for the training set
print("\nCross validation report\n")
print(pd.DataFrame(cross_validation_scores()))

# train the model
train_model()

# get classification report for test set
print("\nClassification report on test data\n")
print(
    classification_report(testLabel,model.predict(testData), target_names=targetNames)
)

# display feature importances
print("\nfeature importances\n")
print_feature_importances()

# plot confision matrix
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt
plot_confusion_matrix(model, testData, testLabel, display_labels=targetNames,cmap='Blues',normalize="true")
plt.show()



