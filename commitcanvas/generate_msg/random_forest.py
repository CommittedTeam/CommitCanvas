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

features = ["commit_type","added","removed","total","num_files","nlocs","is_test","has_md","similarity"]
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
    features, labels, test_size=0.2, random_state=1
)

model = RandomForestClassifier(random_state=1)

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



