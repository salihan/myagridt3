import pandas as pd

class RiceModel:
    def __init__(self):
        self.data = pd.read_csv('datasets/Data_Rice.csv')


    def get_data(self):
        return self.data