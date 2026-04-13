# Librerías
import pandas as pd
from module_data import Dataset
from module_ml import ML_process

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# La funcion main
def main():

    data = Dataset()

    X,y = data.load_xy()
    
    ml = ML_process(X=X, y=y)
    ml.evaluation(LogisticRegression(max_iter=5000))
    ml.evaluation(DecisionTreeClassifier(max_depth=5, min_samples_leaf=20))
    

# Ejectutar el script
if __name__ == "__main__":
    main()