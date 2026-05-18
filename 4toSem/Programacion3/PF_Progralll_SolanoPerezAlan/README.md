# Rendimiento Académico y Gaming — Predicción con ML

**Autor:** Alan Josue Solano Perez | 224164458  
**Materia:** Programación III — UDG  

Predicción de calificaciones académicas a partir de hábitos de vida (gaming, estudio, sueño, asistencia) usando regresión lineal y red neuronal.

---

## Dataset

[Gaming vs Academic Performance](https://www.kaggle.com/datasets/aiexplorer77/gaming-vs-academic-performance) — Kaggle, Asper (2024)  
7,995 registros | 13 variables | Variable objetivo: `grades` (0–118)

---

## Estructura

```
├── data/
│   ├── Gaming_Academic_performance/   # Dataset original
│   └── Data_Limpia_y_Separada/        # X_train, X_test, X_val, y_train, y_test, y_val
├── graficos/                          # Gráficas exportadas del EDA
├── presentaciones/                    # Presentación ejecutiva PDF y PPTX
├── Limpieza de datos.ipynb            # Preprocesamiento
├── Analisis base de datos.ipynb       # EDA y visualizaciones
├── trainer.py                         # Entrenamiento (regresión lineal + red neuronal)
├── predict.py                         # Predicción individual, batch y paralela
├── main.py                            # Pipeline completo
└── requirements.txt
```

---

## Instalación

```bash
pip install -r requirements.txt
```

---

## Uso

```bash
# Ejecutar pipeline completo: entrenar modelos y evaluar
python main.py
```

El script entrena ambos modelos, guarda `data/modelo_nn.keras` e imprime métricas.

Para predecir sobre nuevos datos:

```python
from predict import predecir_desde_dict

resultado = predecir_desde_dict({
    "age": 20, "gaming_hours": 5.0, "study_hours": 4.0,
    "sleep_hours": 7.0, "attendance": 80.0, "social_activity": 2.5,
    "device_usage": 8.0, "reaction_time_ms": 270.0,
    "addiction_score": 10.0, "gender": 1, "gaming_genre": 0, "stress_level": 1
})
```

---

## Resultados

| Métrica | Regresión Lineal | Red Neuronal |
|---|---|---|
| Huber Loss | 5.04 | ~5.10 |
| MSE | 48.66 | ~49.00 |
| MAE | 5.51 | 5.56 |
| R² | **0.905** | ~0.890 |

La relación entre hábitos de vida y calificación es esencialmente **lineal** — la regresión lineal iguala a la red neuronal.

---

## Dependencias principales

- `tensorflow` / `keras`
- `scikit-learn`
- `pandas`, `numpy`
- `matplotlib`, `seaborn`
