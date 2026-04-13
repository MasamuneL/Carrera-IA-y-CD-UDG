import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class ML_process():

    def __init__(self, X, y, seed:int=42):
        self.seed = seed
        self.X = X
        self.y = y

    def evaluation(self, model):
        print(model)
        X_train, X_test, y_train, y_test = train_test_split(self.X,
                                                            self.y,
                                                            test_size=0.2,
                                                            random_state=self.seed)
        # entrenamiento                                                    
        model.fit(X_train,y_train)

        # predicciones
        y_pred = model.predict(X_test)

        # metricas
        acc = accuracy_score(y_pred, y_test)

        # print
        print(f"accuracy: {acc} \n")
