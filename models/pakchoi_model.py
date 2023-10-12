import pandas as pd

class PakchoiModel:
    def __init__(self):
        self.data = pd.read_csv('datasets/Pak_Choy.csv')

    def get_data(self):
        return self.data

    def load_target_data(self):
        return pd.read_csv('datasets/Target_Pak_Choy.csv')

    def load_prediction_data(self):
        return pd.read_csv('datasets/Prediction_Pak_Choy.csv')
