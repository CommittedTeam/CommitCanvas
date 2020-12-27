import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE 
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score, cross_validate
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

features = ["commit_type","modified","added","deleted","num_files","nlocs","is_test","has_md","unique_file_formats"]
data = pd.read_csv("data/training_data.csv",usecols=features)
# encode the labels
target = data["commit_type"]
status = np.array(target)
# Labels are the values we want to predict

targetNames = np.unique(status)
le = LabelEncoder()
labels = le.fit_transform(status)

# Remove the labels from the features
# axis 1 refers to the columns
features = data.drop("commit_type", axis = 1)
# Saving feature names for later use
feature_list = list(features.columns)
# Convert to numpy array
features = np.array(features)

# construct the training and testing splits
(trainData, testData, trainLabel, testLabel) = train_test_split(
    features, labels, test_size=0.2, random_state = 1,stratify=labels
)

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier

model = RandomForestClassifier(random_state=1,max_depth=6)
scv = StratifiedKFold(n_splits=2)

clf = model.fit(trainData,trainLabel)

#Predict the response for test dataset
y_pred = clf.predict(testData)

from sklearn import metrics
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.recall_score(testLabel, y_pred,average="weighted"))

from sklearn.metrics import classification_report

print(
    classification_report(testLabel, y_pred, target_names=targetNames)
)

importances = list(clf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

from sklearn.metrics import confusion_matrix

print(confusion_matrix(testLabel, y_pred, labels=np.unique(labels)))

# see sample classification

feat = ["commit_msg","modified","added","deleted","num_files","nlocs","is_test","has_md","unique_file_formats","diffs_parsed"]
data = pd.read_csv("data/raw_data.csv",usecols=feat)
for i in range(3):
    sample = data.sample()

    msg = sample["commit_msg"]
    labels = np.array(msg)
    diffs = sample["diffs_parsed"]
    parsed_diffs = np.array(diffs)[0]
    sample.drop(columns=['commit_msg', 'diffs_parsed'], inplace=True)

    print("\nSample classifications:\n")
    print("Actual commit message: ",labels[0])
    print("Suggested label: ",le.inverse_transform(clf.predict(sample))[0])


    from ast import literal_eval

    res = literal_eval(parsed_diffs)

    if res["added"]:
        source = res["added"]
    elif res["deleted"]:
        source = res["deleted"]
    else:
        source = None

    # pylint: disable = import-error
    import fixes

    r = fixes.Remove_punctuations()
    document = r.remove(source)
    c = fixes.Sentence_rank()
    out = c.sentence_rank(document)
    print("Suggested commit message:\n",out)


