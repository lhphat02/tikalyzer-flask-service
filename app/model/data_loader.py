import pandas as pd

class Dataloader():

    def __init__(self, json_data: dict):
        self.json_data = json_data
        self.data = pd.DataFrame(json_data)

        # Shuffle
        self.data.sample(frac=1.0, replace=True, random_state=1)

    def get_hd(self):

        return list(self.data.columns.values)

    def get_df(self):

        return self.data