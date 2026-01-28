# E-commerce Dataset (Ecom Expense)

## Descripción General

Este dataset contiene información simulada de transacciones de e-commerce diseñado para fines educativos y de investigación en Machine Learning e Inferencia Bayesiana. Los datos representan el comportamiento de compra de clientes en una plataforma de comercio electrónico, incluyendo características demográficas y de transacción.

## Información del Dataset

- **Nombre del archivo**: `ecom.csv`
- **Número de registros**: 2,362 transacciones
- **Número de variables**: 9 columnas
- **Tipo de datos**: Dataset sintético/simulado
- **Valores faltantes**: Ninguno (dataset completo)

## Fuente y Referencia

**Fuente**: Curso completo de Machine Learning: Data Science en Python  
**Autor**: Juan Gabriel Gomila (joanby)  
**Repositorio**: https://github.com/joanby/python-ml-course  
**Tipo**: Dataset educativo sintético


## Descripción de Variables

| Variable | Tipo | Descripción | Rango/Valores |
|----------|------|-------------|---------------|
| `Transaction ID` | String | Identificador único de transacción | TXN001 - TXN2362 |
| `Age` | Integer | Edad del cliente en años | 20 - 60 años |
| `Items` | Integer | Número de artículos comprados | 1 - 15 items |
| `Monthly Income` | Integer | Ingreso mensual del cliente | Variable |
| `Transaction Time` | Float | Tiempo de la transacción | 0.0 - 999.9 |
| `Record` | Integer | Número de registro/historial | 0 - 10 |
| `Gender` | String | Género del cliente | Female, Male |
| `City Tier` | String | Clasificación de ciudad | Tier 1, Tier 2, Tier 3 |
| `Total Spend` | Float | Gasto total de la transacción | 1,099.82 - 13,944.05 |


## Características del Dataset

### Fortalezas
- **Datos completos**: Sin valores faltantes
- **Estructura clara**: Variables bien definidas y consistentes
- **Diversidad demográfica**: Amplio rango de edades e ingresos
- **Segmentación geográfica**: Sistema de clasificación por tiers de ciudad
- **Tamaño adecuado**: Suficientes observaciones para análisis estadístico

### Limitaciones
- **Datos sintéticos**: No representa comportamiento real de clientes
- **Distribuciones artificiales**: Patrones pueden ser demasiado regulares
- **Contexto limitado**: Falta información sobre productos específicos
- **Temporalidad**: No incluye información temporal detallada

## Casos de Uso Sugeridos

### Análisis Exploratorio
- Segmentación de clientes por demografía
- Análisis de patrones de gasto
- Correlaciones entre variables
- Distribuciones de comportamiento de compra

### Machine Learning
- **Regresión**: Predicción de gasto total (`Total Spend`)
- **Clasificación**: Segmentación de clientes por tier de ciudad
- **Clustering**: Agrupación de clientes por comportamiento
- **Análisis de asociación**: Patrones de compra por demografía

### Inferencia Bayesiana
- Modelado probabilístico de comportamiento de compra
- Estimación de parámetros con incertidumbre
- Análisis de efectos de variables demográficas
- Predicción con intervalos de credibilidad


## Contacto y Soporte

Para preguntas sobre el dataset o el curso:
- **Repositorio original**: https://github.com/joanby/python-ml-course
- **Instructor**: Juan Gabriel Gomila
