import pandas as pd

class Dataloader():

    def __init__(self, csv_path):

        self.csv_path = csv_path
        self.data = pd.read_csv(self.csv_path)

        # Shuffle
        self.data.sample(frac=1.0, replace=True, random_state=1)

    def getHeader(self):

        return list(self.data.columns.values)

    def getFullData(self):

        return self.data