# Dataset CardioGoodFitness

## Información General

**Fuente**: [Kaggle - CardioGoodFitness Dataset](https://www.kaggle.com/datasets/saurav9786/cardiogoodfitness)

**Descripción**: Este dataset contiene información sobre clientes de CardioGoodFitness, una empresa que vende equipos de ejercicio cardiovascular. Los datos incluyen características demográficas de los clientes y su comportamiento de uso de diferentes productos de cintas de correr.

**Tamaño del dataset**: 180 registros (181 líneas incluyendo el header)

## Estructura del Dataset

### Archivo Principal
- **Nombre**: `CardioGoodFitness.csv`
- **Formato**: CSV (Comma Separated Values)
- **Codificación**: UTF-8
- **Separador**: Coma (,)

### Variables/Columnas

| Variable | Tipo | Descripción | Valores Posibles |
|----------|------|-------------|------------------|
| **Product** | Categórica | Modelo de cinta de correr comprada | TM195, TM498, TM798 |
| **Age** | Numérica | Edad del cliente en años | 18-50 años |
| **Gender** | Categórica | Género del cliente | Male, Female |
| **Education** | Numérica | Años de educación completados | 12-21 años |
| **MaritalStatus** | Categórica | Estado civil del cliente | Single, Partnered |
| **Usage** | Numérica | Frecuencia de uso planificada por semana | 2-7 veces |
| **Fitness** | Numérica | Nivel de fitness autoevaluado (escala 1-5) | 1 (Pobre) - 5 (Excelente) |
| **Income** | Numérica | Ingreso anual en dólares | $29,562 - $104,581 |
| **Miles** | Numérica | Millas que planea correr/caminar por semana | 21-360 millas |

## Distribución de Productos

| Producto | Cantidad | Porcentaje | Descripción |
|----------|----------|------------|-------------|
| **TM195** | 80 | 44.4% | Modelo básico/entrada |
| **TM498** | 60 | 33.3% | Modelo intermedio |
| **TM798** | 40 | 22.2% | Modelo premium/avanzado |

## Características por Producto

### TM195 (Modelo Básico)
- **Perfil típico**: Clientes más jóvenes, ingresos menores
- **Rango de ingresos**: ~$29,000 - $45,000
- **Uso típico**: 2-4 veces por semana
- **Fitness promedio**: Niveles 2-4

### TM498 (Modelo Intermedio)
- **Perfil típico**: Clientes de edad media, ingresos moderados
- **Rango de ingresos**: ~$32,000 - $55,000
- **Uso típico**: 3-5 veces por semana
- **Fitness promedio**: Niveles 3-4

### TM798 (Modelo Premium)
- **Perfil típico**: Clientes con mayores ingresos y mejor condición física
- **Rango de ingresos**: ~$48,000 - $105,000
- **Uso típico**: 3-5 veces por semana
- **Fitness promedio**: Niveles 4-5

## Casos de Uso Potenciales

### 1. Análisis de Segmentación de Clientes
- Identificar perfiles de clientes para cada producto
- Desarrollar estrategias de marketing dirigidas
- Optimizar el portafolio de productos

### 2. Modelado Predictivo
- **Clasificación**: Predecir qué producto comprará un cliente basado en sus características
- **Regresión**: Predecir ingresos o millas de uso basado en otras variables
- **Clustering**: Agrupar clientes con características similares

### 3. Análisis de Mercado
- Entender la relación entre demografía y preferencias de producto
- Analizar patrones de uso y fitness
- Identificar oportunidades de mercado

## Consideraciones para el Análisis

### Calidad de los Datos
- **Datos completos**: No hay valores faltantes en la muestra
- **Distribución**: Distribución desigual entre productos (sesgo hacia TM195)

### Limitaciones
- **Tamaño**: Dataset relativamente pequeño (180 registros)
- **Temporalidad**: No hay información temporal (fechas de compra)
- **Geografía**: No hay información geográfica
- **Satisfacción**: No hay métricas de satisfacción del cliente

### Recomendaciones de Preprocesamiento
1. **Encoding categórico**: Convertir variables categóricas (Gender, MaritalStatus, Product)
2. **Normalización**: Considerar normalizar Income y Miles debido a diferentes escalas
3. **Análisis de outliers**: Revisar valores extremos en Income y Miles
4. **Balance de clases**: Considerar técnicas de balanceo si se usa para clasificación

### Preguntas de Investigación
1. ¿Qué características demográficas predicen mejor la elección de producto?
2. ¿Existe correlación entre nivel de fitness e ingresos?
3. ¿Cómo varía el uso planificado entre diferentes segmentos de clientes?
4. ¿Qué factores influyen más en la compra de productos premium?