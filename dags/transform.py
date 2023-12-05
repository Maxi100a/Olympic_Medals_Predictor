import pandas as pd
import pickle
from s3fs.core import S3FileSystem

'''
To Run Locally:
Comment out line 3 (s3fs import statement)
Uncomment line 16 (comment out 13-15): loads in event data from CSV
Uncomment line 42 (comment out 43-45): saves cleaned event data to CSV
'''

DIR = 's3://ece5984-bucket-aedoesma/final_project'

def transform_data():
    # Read data from S3
    s3 = S3FileSystem()
    events = pd.read_pickle(s3.open(f"{DIR}/raw_data.pkl"))
    #events = pd.read_csv('./Data/athlete_events.csv')

    # Remove Irrelevant Columns
    events = events[events.Season != 'Winter']
    events = events.drop(['NOC', 'ID', 'Name', 'Games', 'Season'], axis=1)

    # Replace NaN with 'No Medal'
    events['Medal'] = events['Medal'].fillna('No Medal')

    # still have 166,706 entries 
    events = events.dropna() # drop NA instead of doing average because of differences in builds between the different sports

    # Use Label Encoding for Medal Column
    events['Medal'].replace(['Gold', 'Silver', 'Bronze', 'No Medal'], [1, 2, 3, 4], inplace=True)

    # One-hot encode the remaining categorical features
    encoded_data = pd.get_dummies(events, columns=['Sex', 'Team', 'City', 'Sport', 'Event'])

    # Standardize the numerical values
    encoded_data[['Age', 'Height', 'Weight', 'Year']] = encoded_data[['Age', 'Height', 'Weight', 'Year']].apply(lambda x: (x - x.mean()) / x.std(), axis = 0)

    # save data into a S3 Warehouse
    #encoded_data.to_csv('./Data/processed_events.csv', index=False)
    with s3.open(f"{DIR}/cleaned/processed_events.pkl", "wb") as file:
        file.write(pickle.dumps(encoded_data))