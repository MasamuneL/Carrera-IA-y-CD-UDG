# Datasets de Clasificación de SPAM

Este directorio contiene dos datasets utilizados para tareas de clasificación de mensajes SPAM mediante técnicas de Machine Learning y análisis bayesiano.

## 1. Dataset de Kaggle - SMS Spam Collection (`spam.csv`)

### Descripción
Conjunto de datos reales de mensajes de texto (SMS) recolectados para entrenar y evaluar modelos de clasificación automática de SPAM. Este dataset es ampliamente utilizado en la comunidad de Machine Learning para tareas de clasificación binaria de texto.

### Origen
- **Fuente original**: [grumbletext.co.uk](http://www.grumbletext.co.uk/)
- **Referencia académica**: Almeida, T.A., Gómez Hidalgo, J.M., Yamakami, A. (2011). *Contributions to the Study of SMS Spam Filtering: New Collection and Results*. Proceedings of the ACM Symposium on Document Engineering (DOCENG'11), Mountain View, CA, USA.
- **Implementación inspirada en**: [Naive Bayes + SVM Spam Filtering](https://www.kaggle.com/code/pablovargas/naive-bayes-svm-spam-filtering) por Pablo Vargas

### Estructura
- **Formato**: CSV con separador por comas
- **Columnas**:
  - `v1`: Etiqueta de clasificación (`ham` = no spam, `spam` = spam)
  - `v2`: Contenido completo del mensaje SMS
  - Columnas adicionales vacías (v3, v4, v5)
- **Tamaño**: ~503KB
- **Casos de uso**: Clasificación binaria, análisis de texto, filtrado automático de mensajes

### Características
- Datos reales de mensajes SMS
- Etiquetas balanceadas entre spam y ham
- Texto en inglés con variaciones de escritura típicas de SMS
- Ideal para técnicas como Naive Bayes, SVM, y otros algoritmos de clasificación de texto

## 2. Dataset Ficticio (`spam_ficticio.csv`)

### Descripción
Dataset sintético creado con fines didácticos para demostrar conceptos básicos de clasificación de SPAM utilizando características específicas de palabras.

### Estructura
- **Formato**: CSV con separador por comas
- **Primera fila**: Nombres de características (palabras clave)
  - `congratulations`, `you`, `won`, `free`, `gift`, `attached`, `sincerely`, `thanks`, `spam`
- **Filas siguientes**: Valores binarios (0/1) indicando presencia/ausencia de cada palabra
- **Tamaño**: ~245 bytes
- **Última columna**: Variable objetivo (1 = spam, 0 = ham)

### Características
- Datos binarios simplificados
- 8 características de palabras + 1 variable objetivo
- Ideal para ejemplos introductorios de clasificación
- Perfecto para demostrar algoritmos como Naive Bayes en su forma más básica


## Consideraciones
- Ambos datasets están diseñados para clasificación binaria
- El dataset de Kaggle requiere preprocesamiento de texto
- El dataset ficticio está listo para usar con algoritmos que manejan características binarias
- Ideal para comparar rendimiento entre datos sintéticos y reales
