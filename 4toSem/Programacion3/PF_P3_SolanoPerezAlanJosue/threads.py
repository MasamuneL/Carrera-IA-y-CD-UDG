import os
import numpy as np
import pandas as pd
import tensorflow as tf
from concurrent.futures import ThreadPoolExecutor, as_completed

MODEL_PATH = "data/modelo_nn.keras"

FEATURE_COLS = [
    "age", "gaming_hours", "study_hours", "sleep_hours",
    "attendance", "social_activity", "device_usage",
    "reaction_time_ms", "addiction_score", "gender",
    "gaming_genre", "stress_level",
]


def cargar_modelo(model_path=MODEL_PATH):
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"No se encontro el modelo en '{model_path}'. Ejecuta primero el entrenamiento."
        )
    return tf.keras.models.load_model(model_path)


def predecir(features, model=None, model_path=MODEL_PATH):
    """
    features: lista o array de 12 valores en el orden de FEATURE_COLS.
    model: modelo ya cargado (opcional, evita recarga).
    Retorna la calificacion predicha (float).
    """
    if model is None:
        model = cargar_modelo(model_path)
    x = np.asarray(features, dtype=np.float32).reshape(1, len(FEATURE_COLS))
    return float(model.predict(x, verbose=0)[0][0])


def predecir_batch(features_list, model_path=MODEL_PATH):
    """
    Prediccion batch nativa de TF — mas rapido para muchas filas.
    features_list: lista de listas / array (N, 12).
    Retorna array de N predicciones.
    """
    model = cargar_modelo(model_path)
    X = np.asarray(features_list, dtype=np.float32)
    preds = model.predict(X, verbose=0).flatten()
    return preds.tolist()


def predecir_paralelo(features_list, workers=4, model_path=MODEL_PATH):
    """
    Prediccion paralela con ThreadPoolExecutor.
    Carga el modelo una sola vez y distribuye filas entre hilos.
    Util cuando las entradas llegan de fuentes distintas.
    features_list: lista de listas (N, 12).
    Retorna lista de predicciones en el mismo orden.
    """
    model = cargar_modelo(model_path)
    results = [None] * len(features_list)

    def _predict_one(idx, features):
        return idx, predecir(features, model=model)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_predict_one, i, f): i
            for i, f in enumerate(features_list)
        }
        for future in as_completed(futures):
            idx, pred = future.result()
            results[idx] = pred

    return results


def predecir_desde_dict(datos: dict, model_path=MODEL_PATH):
    """
    datos: dict con llaves iguales a FEATURE_COLS.
    """
    features = [datos[col] for col in FEATURE_COLS]
    return predecir(features, model_path=model_path)


def predecir_desde_csv(csv_path, row_index=0, model_path=MODEL_PATH):
    """Carga una fila del CSV y predice su calificacion."""
    data = pd.read_csv(csv_path)
    row = data.iloc[row_index][FEATURE_COLS].astype(np.float32).to_numpy()
    pred = predecir(row, model_path=model_path)
    print(f"Fila {row_index} -> Calificacion predicha: {pred:.4f}")
    return pred


def predecir_csv_paralelo(csv_path, workers=4, model_path=MODEL_PATH):
    """
    Carga todo el CSV y predice todas las filas en paralelo.
    Retorna DataFrame con columna 'prediccion'.
    """
    data = pd.read_csv(csv_path)
    features_list = data[FEATURE_COLS].astype(np.float32).values.tolist()
    preds = predecir_paralelo(features_list, workers=workers, model_path=model_path)
    data["prediccion"] = preds
    return data
