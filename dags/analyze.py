import pickle
from sklearn.metrics import accuracy_score

def analyze_models(X_test, y_test):
    mlp = pickle.load(open('./models/mlp.pickle', 'rb'))
    mlp_predictions = mlp.predict(X_test)

    clf = pickle.load(open('./models/clf.pickle', 'rb'))
    clf_predictions = clf.predict(X_test)

    knn = pickle.load(open('./models/knn.pickle', 'rb'))
    knn_predictions = knn.predict(X_test)

    print(f"MLP Accuracy Score: {accuracy_score(y_test, mlp_predictions):.2%}")
    print(f"CLF Accuracy Score: {accuracy_score(y_test, clf_predictions):.2%}")
    print(f"KNN Accuracy Score: {accuracy_score(y_test, knn_predictions):.2%}")


analyze_models()