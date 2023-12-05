import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from s3fs.core import S3FileSystem

"""
To run locally:
Comment out line 9 (s3fs import statement)
Uncomment lines 23, 33, and 43 to save models locally
Uncomment lines 77-79
Comment lines 66, 82-88 (S3 saving code)
Uncomment lines 97 98 (Test set saving code)
Comment lines 93-86
"""

DIR = 's3://ece5984-bucket-aedoesma/final_project'

def build_MLP_classifier(X_train, y_train):
    # Build and fit the Multi-Layer Perceptron model to the data
    mlp = MLPClassifier(random_state=1, max_iter=200)
    mlp.fit(X_train, y_train)

    # Save model locally
    # pickle.dump(mlp, open('./models/mlp.pkl', 'wb'))

    return mlp

def build_DT_classifier(X_train, y_train):
    # Build and fit a Decision Tree model to the data
    clf = DecisionTreeClassifier(criterion='log_loss', random_state=1)
    clf.fit(X_train, y_train)

    # Save model locally
    # pickle.dump(clf, open('./models/clf.pkl', 'wb'))

    return clf

def build_KNN_classifier(X_train, y_train):
    # Build and fit a K-Nearest Neighbors model to the data
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)

    # Save model locally
    # pickle.dump(knn, open('./models/knn.pkl', 'wb'))

    return knn

def build_RF_classifier(X_train, y_train):
    # build and fit a Random Forest Classifier model to the data
    rf = RandomForestClassifier(random_state=1, n_estimators=100)
    rf.fit(X_train, y_train)

    # Save model locally
    #pickle.dump(rf, open('./models/rf.pkl', 'wb'))

    return rf

def build_models():
    # Read in the processed CSV and split it into training & testing sets
    s3 = S3FileSystem()
    data = pd.read_pickle(s3.open(f'{DIR}/cleaned/processed_events.pkl'))
    # data = pd.read_csv('./Data/processed_events.csv')

    X = data.drop('Medal', axis=1)
    y = data['Medal']

    split_data = train_test_split(X, y, stratify=y, random_state=1)
    X_train, X_test, y_train, y_test = split_data

    # Build and save the different classifier models
    # build_MLP_classifier(X_train, y_train)
    # build_DT_classifier(X_train, y_train)
    # build_KNN_classifier(X_train, y_train)
    # build_RF_classifier(X_train, y_train)

    DIR_models = f'{DIR}/models'
    with s3.open(f"{DIR_models}/mlp.pkl", 'wb') as file:
        file.write(pickle.dumps(build_MLP_classifier(X_train, y_train)))
    with s3.open(f"{DIR_models}/clf.pkl", 'wb') as file:
        file.write(pickle.dumps(build_DT_classifier(X_train, y_train)))
    with s3.open(f"{DIR_models}/knn.pkl", 'wb') as file:
        file.write(pickle.dumps(build_KNN_classifier(X_train, y_train)))
    with s3.open(f"{DIR_models}/rf.pkl", 'wb') as file:
        file.write(pickle.dumps(build_RF_classifier(X_train, y_train)))

    # Save the test sets for analyzing
    with s3.open(f"{DIR}/cleaned/X_test.pkl", "wb") as file:
        file.write(pickle.dumps(X_test))
    with s3.open(f"{DIR}/cleaned/y_test.pkl", "wb") as file:
        file.write(pickle.dumps(y_test))

    # Save locally
    # pickle.dump(X_test, open("./data/X_test.pkl", "wb"))
    # pickle.dump(y_test, open("./data/y_test.pkl", "wb"))