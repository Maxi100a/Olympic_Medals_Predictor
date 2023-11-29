import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import pickle

def preprocess_data():
    data = pd.read_csv('./Data/cleaned_events.csv')
    
    # Remove name column
    data = data.drop('Name', axis=1)

    # Columns needed to encode
    # Sex, Team, City, Sport, Event, Medal

    # Use Label Encoding for Medal column
    data['Medal'].replace(['Gold', 'Silver', 'Bronze', 'No Medal'], [1, 2, 3, 4], inplace=True)

    # One-hot encode the remaining categorical features
    encoded_data = pd.get_dummies(data, columns=['Sex', 'Team', 'City', 'Sport', 'Event'])
    
    # Standardize the numerical values
    encoded_data[['Age', 'Height', 'Weight', 'Year']] = encoded_data[['Age', 'Height', 'Weight', 'Year']].apply(lambda x: (x - x.mean()) / x.std(), axis = 0)
    
    return encoded_data

def build_MLP_classifier(data):
    X = data.drop('Medal', axis=1)
    y = data['Medal']

    X_train, _, y_train, _ = train_test_split(X, y, random_state=1)

    # Build and fit the Multi-Layer Perceptron to the data
    mlp = MLPClassifier(random_state=1, max_iter=150, verbose=True)
    mlp.fit(X_train, y_train)
    
    # Save model
    pickle.dump(mlp, open('./Models/mlp.pickle', 'wb'))

def analyze_models(data):
    X = data.drop('Medal', axis=1)
    y = data['Medal']

    _, X_test, _, y_test = train_test_split(X, y, random_state=1)
        
    mlp = pickle.load(open('./Models/mlp.pickle', 'rb'))
    predictions = mlp.predict(X_test)

    print(f"Accuracy Score: {accuracy_score(y_test, predictions):.2%}")
    cm = confusion_matrix(y_test, predictions, labels=mlp.classes_)
    disp = ConfusionMatrixDisplay(cm, display_labels=mlp.classes_)

    disp.plot()
    plt.show()


data = preprocess_data()
build_MLP_classifier(data)
analyze_models(data)

