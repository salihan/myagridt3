import pandas as pd

class HomeModel:
    def __init__(self):
        self.data = pd.read_csv('datasets/home.csv')

    def get_data(self):
        return self.data
