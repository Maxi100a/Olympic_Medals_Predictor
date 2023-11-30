import os
from s3fs.core import S3FileSystem
from kaggle.api.kaggle_api_extended import KaggleApi
import pickle
import pandas as pd

"""
To run locally:
Comment out line 2 (s3fs import statement)
Comment out 22-26 (file already downloads to machine, these lines are just for pushing onto S3)
"""

def download_data():
    # authenticate kaggle API & download olympics dataset
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('heesoo37/120-years-of-olympic-history-athletes-and-results', './Data/', unzip=True)

    # delete the unused noc_regions csv file (save space)
    os.remove('./Data/noc_regions.csv')

    # push to S3 data lake (file already on machine)
    events = pd.read_csv('./Data/athlete_events.csv')
    s3 = S3FileSystem()
    DIR = 's3://ece5984-bucket-aedoesma/final_project'
    with s3.open(f"{DIR}/raw_data.pkl", 'wb') as file:
        file.write(pickle.dumps(events))


    
