import pickle
from sklearn.metrics import accuracy_score
from s3fs.core import S3FileSystem

def analyze_models():
    s3 = S3FileSystem()
    DIR = 's3://ece5984-bucket-aedoesma/final_project'
    X_test = pickle.load(s3.open(f'{DIR}/cleaned/X_test.pkl', 'rb'))
    y_test = pickle.load(s3.open(f'{DIR}/cleaned/y_test.pkl', 'rb'))

    mlp = pickle.load(s3.open(f'{DIR}/models/mlp.pkl', 'rb'))
    mlp_predictions = mlp.predict(X_test)

    clf = pickle.load(s3.open(f'{DIR}/models/clf.pkl', 'rb'))
    clf_predictions = clf.predict(X_test)

    knn = pickle.load(s3.open(f'{DIR}/models/knn.pkl', 'rb'))
    knn_predictions = knn.predict(X_test)

    rf = pickle.load(s3.open(f'{DIR}/models/rf.pkl', 'rb'))
    rf_predictions = rf.predict(X_test)

    print(f"MLP Accuracy Score: {accuracy_score(y_test, mlp_predictions):.2%}")
    print(f"CLF Accuracy Score: {accuracy_score(y_test, clf_predictions):.2%}")
    print(f"KNN Accuracy Score: {accuracy_score(y_test, knn_predictions):.2%}")
    print(f"RF Accuracy Score: {accuracy_score(y_test, rf_predictions):.2%}")

def analyze_models_local():
    X_test = pickle.load(open('./data/X_test.pkl', 'rb'))
    y_test = pickle.load(open('./data/y_test.pkl', 'rb'))

    mlp = pickle.load(open('./models/mlp.pkl', 'rb'))
    mlp_predictions = mlp.predict(X_test)

    clf = pickle.load(open('./models/clf.pkl', 'rb'))
    clf_predictions = clf.predict(X_test)

    knn = pickle.load(open('./models/knn.pkl', 'rb'))
    knn_predictions = knn.predict(X_test)

    rf = pickle.load(open('./models/rf.pkl', 'rb'))
    rf_predictions = rf.predict(X_test)

    print(f"MLP Accuracy Score: {accuracy_score(y_test, mlp_predictions):.2%}")
    print(f"CLF Accuracy Score: {accuracy_score(y_test, clf_predictions):.2%}")
    print(f"KNN Accuracy Score: {accuracy_score(y_test, knn_predictions):.2%}")
    print(f"rf Accuracy Score: {accuracy_score(y_test, rf_predictions):.2%}")