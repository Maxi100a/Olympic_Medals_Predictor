import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi


def download_data():
    # Initialize and authenticate kaggle API & download olympics dataset
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('heesoo37/120-years-of-olympic-history-athletes-and-results', './Data/', unzip=True)


def EDA():
    events = pd.read_csv('./Data/athlete_events.csv')
    # regions = pd.read_csv('./Data/noc_regions.csv')

    print(events.info())
    # print(regions)

    # Remove Irrelevant Columns
    events = events.drop(['NOC', 'ID'], axis=1)
    events = events[events.Season != 'Winter']
    print(events)

# Uncomment to download the data
# download_data()


EDA()
