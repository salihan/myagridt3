import pandas as pd

class RiceModel:
    def __init__(self):
        self.data = pd.read_csv('datasets/Data_Rice.csv', index_col=[0])


    def get_data(self):
        return self.data