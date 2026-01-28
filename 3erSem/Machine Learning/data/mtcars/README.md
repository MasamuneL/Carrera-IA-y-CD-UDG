# Dataset Motor Trend Car Road Tests (mtcars)

## Descripción General

El dataset `mtcars.csv` contiene datos extraídos de la revista Motor Trend US de 1974, que incluye el consumo de combustible y 10 aspectos del diseño y rendimiento de automóviles para 32 automóviles (modelos 1973-74).

Este es uno de los datasets más utilizados en estadística y ciencia de datos para ejemplos y análisis exploratorio.

## Información del Dataset

- **Número de observaciones**: 32 automóviles
- **Número de variables**: 11 variables
- **Formato**: CSV (Comma Separated Values)
- **Fuente original**: Henderson and Velleman (1981), Building multiple regression models interactively. Biometrics, 37, 391–411.

## Descripción de Variables

| Variable | Descripción | Unidades | Tipo |
|----------|-------------|----------|------|
| `model` | Nombre del modelo de automóvil | - | Categórica |
| `mpg` | Millas por galón (consumo de combustible) | millas/galón | Numérica continua |
| `cyl` | Número de cilindros | - | Numérica discreta |
| `disp` | Desplazamiento del motor | pulgadas cúbicas | Numérica continua |
| `hp` | Caballos de fuerza brutos | hp | Numérica continua |
| `drat` | Relación del eje trasero | - | Numérica continua |
| `wt` | Peso del automóvil | 1000 libras | Numérica continua |
| `qsec` | Tiempo en 1/4 de milla | segundos | Numérica continua |
| `vs` | Forma del motor (0 = V-shaped, 1 = straight) | - | Binaria |
| `am` | Tipo de transmisión (0 = automática, 1 = manual) | - | Binaria |
| `gear` | Número de marchas hacia adelante | - | Numérica discreta |
| `carb` | Número de carburadores | - | Numérica discreta |

## Estadísticas Descriptivas Básicas

### Variables Numéricas Principales:
- **MPG (Consumo)**: Rango de 10.4 a 33.9 millas por galón
- **Cilindros**: 4, 6 u 8 cilindros
- **Caballos de fuerza**: Rango de 52 a 335 hp
- **Peso**: Rango de 1.513 a 5.424 (en miles de libras)

### Variables Categóricas:
- **Transmisión**: 19 automáticos, 13 manuales
- **Forma del motor**: 18 en V, 14 rectos
- **Marchas**: 3, 4 o 5 marchas
- **Carburadores**: 1 a 8 carburadores

## Casos de Uso Comunes

Este dataset es ideal para:

1. **Análisis de regresión**: Predecir el consumo de combustible (mpg) basado en otras características
2. **Análisis exploratorio de datos**: Visualización de relaciones entre variables
3. **Clustering**: Agrupar automóviles por características similares
4. **Análisis de correlación**: Estudiar relaciones entre variables del rendimiento automotriz
5. **Pruebas estadísticas**: Comparar grupos (automático vs manual, etc.)
6. **Aprendizaje automático**: Dataset de práctica para algoritmos supervisados

## Ejemplos de Preguntas de Investigación

- ¿Cómo afecta el peso del automóvil al consumo de combustible?
- ¿Los automóviles con transmisión manual tienen mejor rendimiento de combustible?
- ¿Existe relación entre el número de cilindros y los caballos de fuerza?
- ¿Qué características predicen mejor el consumo de combustible?

## Consideraciones y Limitaciones

- Los datos son de 1974, por lo que pueden no ser representativos de automóviles modernos
- El tamaño de muestra es relativamente pequeño (32 observaciones)
- Todos los automóviles son de marcas estadounidenses de la época
- Algunas variables pueden estar correlacionadas (multicolinealidad)

## Referencias

- Henderson, H. V. and Velleman, P. F. (1981). Building multiple regression models interactively. *Biometrics*, 37, 391–411.
- Motor Trend Magazine, 1974
