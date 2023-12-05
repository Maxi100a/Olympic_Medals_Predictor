import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
# from s3fs.core import S3FileSystem

DIR = 's3://ece5984-bucket-aedoesma/final_project' # S3 landing location

def generate_confusion_matrix(y_test, y_pred, model_name, dir=None):
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Create and plot confusion matrix
    cm = confusion_matrix(y_test, y_pred, normalize='true')
    cmap = sns.dark_palette("purple", as_cmap=True,)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='.2%', cmap=cmap, cbar=True, linewidths=.5, square=True, vmax=np.max(cm), vmin=0,)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title(f'{model_name} Confusion Matrix: Accuracy: {accuracy:.2%}')
    
    if dir is not None:
        plt.savefig(dir)
    else:
        plt.show()


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

    with tempfile.TemporaryDirectory() as tempdir:
        generate_confusion_matrix(y_test, mlp_predictions, "Multi-Layer Perceptron", f"{tempdir}/mlp.png")
        generate_confusion_matrix(y_test, clf_predictions, "Decision Tree", f"{tempdir}/dt.png")
        generate_confusion_matrix(y_test, knn_predictions, "K-Nearest Neighbors", f"{tempdir}/knn.png")
        generate_confusion_matrix(y_test, rf_predictions, "Random Forest", f"{tempdir}/rf.png")

        models = ['mlp', 'dt', 'knn', 'rf']
        for model in models:
            s3.put(f"{tempdir}/{model}.png", f"{DIR}/confusion_matrices/{model}.png")

def analyze_models_local():
    X_test = pickle.load(open('./data/X_test.pkl', 'rb'))
    y_test = pickle.load(open('./data/y_test.pkl', 'rb'))

    mlp = pickle.load(open('./models/mlp.pickle', 'rb'))
    mlp_predictions = mlp.predict(X_test)

    clf = pickle.load(open('./models/clf.pickle', 'rb'))
    clf_predictions = clf.predict(X_test)

    knn = pickle.load(open('./models/knn.pickle', 'rb'))
    knn_predictions = knn.predict(X_test)

    rf = pickle.load(open('./models/rf.pkl', 'rb'))
    rf_predictions = rf.predict(X_test)

    generate_confusion_matrix(y_test, mlp_predictions, 'Multi-Layer Peceptron',"./Images/mlp.png")
    generate_confusion_matrix(y_test, clf_predictions, 'Decision Tree',"./Images/dt.png")
    generate_confusion_matrix(y_test, knn_predictions, 'K-Nearest Neighbors',"./Images/knn.png")
    generate_confusion_matrix(y_test, rf_predictions, 'Random Forest',"./Images/rf.png")