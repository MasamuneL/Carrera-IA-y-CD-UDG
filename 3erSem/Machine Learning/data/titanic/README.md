# Dataset del Titanic

## Descripción
Este dataset contiene información sobre los pasajeros del RMS Titanic, que se hundió en su viaje inaugural el 15 de abril de 1912 después de chocar con un iceberg. El hundimiento del Titanic resultó en la muerte de 1502 de los 2224 pasajeros y tripulantes, convirtiéndose en uno de los desastres marítimos más mortíferos en tiempos de paz.

Este dataset es ampliamente utilizado en el campo del aprendizaje automático y la inferencia bayesiana como un problema de clasificación para predecir la supervivencia de los pasajeros.

## Origen
El dataset fue descargado de Kaggle: [Titanic Dataset](https://www.kaggle.com/datasets/sakshisatre/titanic-dataset)

## Contenido
El archivo `titanic.csv` contiene los siguientes campos:

| Variable | Descripción |
|----------|-------------|
| pclass | Clase del pasajero (1 = 1ra clase, 2 = 2da clase, 3 = 3ra clase) |
| survived | Supervivencia (0 = No, 1 = Sí) |
| name | Nombre del pasajero |
| sex | Sexo del pasajero |
| age | Edad del pasajero en años |
| sibsp | Número de hermanos/cónyuges a bordo |
| parch | Número de padres/hijos a bordo |
| ticket | Número de boleto |
| fare | Tarifa del pasajero |
| cabin | Número de cabina |
| embarked | Puerto de embarque (C = Cherbourg, Q = Queenstown, S = Southampton) |
| boat | Bote salvavidas (si sobrevivió) |
| body | Número de identificación del cuerpo (si no sobrevivió y fue recuperado) |
| home.dest | Hogar/Destino |

## Uso potencial
Este dataset puede ser utilizado para:

1. **Análisis exploratorio de datos**: Examinar las relaciones entre diferentes variables y la tasa de supervivencia.
2. **Modelado predictivo**: Construir modelos para predecir qué pasajeros sobrevivieron al naufragio.
3. **Inferencia bayesiana**: Aplicar métodos bayesianos para estimar la probabilidad de supervivencia basada en diferentes características.
4. **Visualización de datos**: Crear visualizaciones informativas sobre los factores que influyeron en la supervivencia.

## Características interesantes
- La tasa de supervivencia varía significativamente según la clase socioeconómica, el sexo y la edad.
- El famoso lema "las mujeres y los niños primero" puede ser analizado con estos datos.
- Los patrones de supervivencia familiar pueden ser estudiados usando las variables sibsp y parch.

## Contexto histórico
El RMS Titanic era un transatlántico británico que se hundió en el Océano Atlántico Norte después de chocar con un iceberg durante su viaje inaugural desde Southampton a Nueva York. De los aproximadamente 2,224 pasajeros y tripulantes a bordo, más de 1,500 murieron, lo que convirtió al hundimiento en uno de los desastres marítimos comerciales en tiempos de paz más mortíferos de la historia moderna.

## Notas
- Algunos registros pueden tener valores faltantes, especialmente en campos como 'age', 'cabin', 'boat' y 'body'.
- Este dataset es comúnmente utilizado para enseñar técnicas de manejo de datos faltantes y preprocesamiento de datos.
