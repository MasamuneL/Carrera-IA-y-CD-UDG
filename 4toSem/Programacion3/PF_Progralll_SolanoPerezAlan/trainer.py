import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def cargar_dataset():
    # Establecer ruta del dataset y codificar los datos
    X_train = pd.read_csv('data/Data_Limpia_y_Separada/X_train.csv')
    X_test  = pd.read_csv('data/Data_Limpia_y_Separada/X_test.csv')
    X_val   = pd.read_csv('data/Data_Limpia_y_Separada/X_val.csv')
    y_train = pd.read_csv('data/Data_Limpia_y_Separada/y_train.csv').squeeze()
    y_test  = pd.read_csv('data/Data_Limpia_y_Separada/y_test.csv').squeeze()
    y_val   = pd.read_csv('data/Data_Limpia_y_Separada/y_val.csv').squeeze()
    return X_train, X_test, y_train, y_test, X_val, y_val

def construir_modelo(input_shape):
    # Definir modelo
    model = tf.keras.Sequential(
        [
            # Estructura del modelo en capas
            tf.keras.layers.Input(shape=(input_shape,)),
            tf.keras.layers.Dense(128, activation='linear'),
            #tf.keras.layers.Dense(64, activation='linear'),
            tf.keras.layers.Dense(1),
        ]
    )

    model.compile(
        optimizer="adamw",
        loss="huber",
        metrics=["mae",tf.keras.metrics.R2Score()],
        )
    return model

def entrenar_modelo(model, X_train, y_train, X_test, y_test):
    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=32,
        validation_data=(X_test, y_test),
        verbose=1
    )
    return history

def guardar_modelo(model, path='data/modelo_nn.keras'):
    model.save(path)
    return "Modelo guardado exitosamente"

def regresion_lineal(X_train, y_train, X_test, y_test):
    # Entrenar regresion lineal con sklearn
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)
    print(f"Regresion Lineal — MSE: {mse:.4f} | R2: {r2:.4f}")
    return lr
