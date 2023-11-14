import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi


def download_data():
    # Initialize and authenticate kaggle API & download olympics dataset
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('heesoo37/120-years-of-olympic-history-athletes-and-results', './Data/', unzip=True)


def transform_data():
    events = pd.read_csv('./Data/athlete_events.csv')
    # regions = pd.read_csv('./Data/noc_regions.csv')

    print(events.info())
    # print(regions)

    # Remove Irrelevant Columns
    events = events.drop(['NOC', 'ID'], axis=1)
    events = events[events.Season != 'Winter']
    print(events.info())

    # Replace NaN with 'No Medal'
    events['Medal'] = events['Medal'].fillna('No Medal')
    print(events.groupby('Year'))

    # There are significant missing NAs in age, height and weight at 9,189, 51,857, and 53,854 values respectively
    print(events[events.isnull().any(axis=1)].sort_values(by="Year"))

    # events = events.drop(events[events.isnull().any(axis=1)])

    # still have 166,706 entries 
    events = events.dropna() # drop NA instead of doing average because of differences in builds between the different sports

    # save data into a csv file
    events.to_csv('./Data/cleaned_events.csv')

# Uncomment to download the data
# download_data()

transform_data()
