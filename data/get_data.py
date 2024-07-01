import kaggle as kg
import pandas as pd
import os

os.environ['KAGGLE_USERNAME'] = 'togetherthoughh'
os.environ['KAGGLE_KEY'] = 'eab42567f71e0dc998ba5ed72e4e55ed'

kg.api.authenticate()

kg.api.dataset_download_files(dataset = "mohamedmustafa/real-life-violence-situations-dataset", path='videos', unzip=True)