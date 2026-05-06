import pandas as pd
import numpy as np
import tensorflow as tf

def cargar_dataset():
    # Establecer ruta del dataset y codificar los datos
    data = pd.read_csv('data/Gaming_Academic_performance/Gaming_Academic_Performance.csv')
    age = data['Age'].astype(np.float32).to_numpy()

    # Limpiar datos
    print(np.mean(age))
    return age

def construir_modelo(num_classes):
    # Definir modelo
    model = tf.keras.Sequential(
        [
            # Estructura del modelo en capas
            tf.keras.layers.Input(shape=12),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(num_classes, activation='softmax'),
        ]
    )

    model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["accuracy"],
        )
    return model

def entrenar_modelo():
    return "Modelo entrenado exitosamente"

def guardar_modelo():
    return "Modelo guardado exitosamente"
