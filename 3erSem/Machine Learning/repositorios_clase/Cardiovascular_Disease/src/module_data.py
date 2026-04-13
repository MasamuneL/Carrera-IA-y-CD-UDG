# Preprocesamiento de datos

import pandas as pd

class Dataset():
    
    # Constructor
    def __init__(self, n_samples:int=None):
        self.n_samples = n_samples

    def load(self):
        df = pd.read_csv("../data/Cardiovascular_Disease_Dataset.csv")
        df = df.drop(columns="patientid")

        if self.n_samples:
            df = df.sample(n=self.n_samples)

        return df
    
    def load_xy(self):
        df = self.load()

        X = df.drop(columns="target")
        y = df["target"]

        return X,y
