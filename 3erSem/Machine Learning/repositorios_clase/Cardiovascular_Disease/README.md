# Cardiovascular Disease Classification

Un proyecto de machine learning para la clasificación de enfermedades cardiovasculares utilizando técnicas de aprendizaje supervisado.

## Descripción

Este proyecto implementa un pipeline completo de machine learning para predecir la presencia de enfermedades cardiovasculares en pacientes basándose en características clínicas. Se utilizan algoritmos de clasificación como Regresión Logística y Árboles de Decisión para evaluar el riesgo cardiovascular.

## Estructura del Proyecto

```
Cardiovascular_Disease/
├── data/
│   ├── Cardiovascular_Disease_Dataset.csv
│   └── .gitkeep
├── src/
│   ├── main.py              # Script principal
│   ├── module_data.py       # Módulo de procesamiento de datos
│   └── module_ml.py         # Módulo de machine learning
├── LICENSE
└── README.md
```

## Dataset

El dataset contiene información clínica de pacientes con las siguientes características:

- **age**: Edad del paciente
- **gender**: Género (0: femenino, 1: masculino)
- **chestpain**: Tipo de dolor en el pecho
- **restingBP**: Presión arterial en reposo
- **serumcholestrol**: Colesterol sérico
- **fastingbloodsugar**: Azúcar en sangre en ayunas
- **restingrelectro**: Resultados del electrocardiograma en reposo
- **maxheartrate**: Frecuencia cardíaca máxima alcanzada
- **exerciseangia**: Angina inducida por ejercicio
- **oldpeak**: Depresión del ST inducida por ejercicio
- **slope**: Pendiente del segmento ST
- **noofmajorvessels**: Número de vasos principales
- **target**: Variable objetivo (0: sin enfermedad, 1: con enfermedad)

## Modelos Implementados

- **Regresión Logística**: Modelo lineal para clasificación binaria
- **Árbol de Decisión**: Modelo basado en reglas con parámetros optimizados

## Uso

### Requisitos

```bash
pip install pandas scikit-learn
```

### Ejecución

```bash
cd src
python main.py
```

## Módulos

### `module_data.py`
- **Dataset**: Clase para cargar y preprocesar los datos
  - `load()`: Carga el dataset completo
  - `load_xy()`: Separa características (X) y variable objetivo (y)

### `module_ml.py`
- **ML_process**: Clase para el procesamiento de machine learning
  - `evaluation()`: Entrena y evalúa modelos usando train/test split

## Resultados

El proyecto evalúa automáticamente ambos modelos y muestra la precisión (accuracy) de cada uno en el conjunto de prueba.

## Licencia

Este proyecto está bajo la licencia especificada en el archivo LICENSE.
