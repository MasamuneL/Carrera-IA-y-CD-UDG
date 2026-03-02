# Customer Churn Dataset

## Descripción General

Este dataset contiene información sobre clientes de una empresa de telecomunicaciones y su comportamiento de abandono (churn). El objetivo principal es predecir qué clientes tienen mayor probabilidad de cancelar sus servicios basándose en sus patrones de uso y características demográficas.

## Información del Dataset

- **Archivo**: `customer_churn_model.txt`
- **Formato**: CSV (separado por comas)
- **Número de registros**: 3,332 clientes
- **Número de características**: 21 variables
- **Variable objetivo**: `Churn?` (True/False)

## Descripción de Variables

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `State` | Categórica | Estado de residencia del cliente (código de 2 letras) |
| `Account Length` | Numérica | Duración de la cuenta en días |
| `Area Code` | Categórica | Código de área telefónico |
| `Phone` | Categórica | Número de teléfono (formato XXX-XXXX) |
| `Int'l Plan` | Categórica | Plan internacional (yes/no) |
| `VMail Plan` | Categórica | Plan de correo de voz (yes/no) |
| `VMail Message` | Numérica | Número de mensajes de correo de voz |
| `Day Mins` | Numérica | Minutos de uso durante el día |
| `Day Calls` | Numérica | Número de llamadas durante el día |
| `Day Charge` | Numérica | Cargos por llamadas durante el día |
| `Eve Mins` | Numérica | Minutos de uso durante la tarde |
| `Eve Calls` | Numérica | Número de llamadas durante la tarde |
| `Eve Charge` | Numérica | Cargos por llamadas durante la tarde |
| `Night Mins` | Numérica | Minutos de uso durante la noche |
| `Night Calls` | Numérica | Número de llamadas durante la noche |
| `Night Charge` | Numérica | Cargos por llamadas durante la noche |
| `Intl Mins` | Numérica | Minutos de llamadas internacionales |
| `Intl Calls` | Numérica | Número de llamadas internacionales |
| `Intl Charge` | Numérica | Cargos por llamadas internacionales |
| `CustServ Calls` | Numérica | Número de llamadas al servicio al cliente |
| `Churn?` | Binaria | Variable objetivo: True si el cliente abandonó, False si no |

## Características del Dataset

### Distribución de Clases
- **No Churn (False)**: Mayoría de los registros
- **Churn (True)**: Minoría de los registros

### Variables Categóricas
- **State**: 50+ estados diferentes de EE.UU.
- **Area Code**: Principalmente 415, 408, 510
- **Int'l Plan**: Binaria (yes/no)
- **VMail Plan**: Binaria (yes/no)

### Variables Numéricas
- Todas las variables de minutos, llamadas y cargos son continuas
- Las variables de cargos están correlacionadas con los minutos correspondientes
- `Account Length` varía desde días hasta varios años

## Casos de Uso

Este dataset es ideal para:

1. **Análisis Predictivo**: Modelos de clasificación binaria para predecir churn
2. **Análisis Exploratorio**: Identificar patrones en el comportamiento de clientes
3. **Segmentación de Clientes**: Agrupar clientes por comportamiento de uso
4. **Análisis de Retención**: Estrategias para reducir la tasa de abandono
5. **Machine Learning**: Entrenamiento de algoritmos de clasificación

## Consideraciones de Preprocesamiento

1. **Variables Categóricas**: Requieren encoding (One-Hot o Label Encoding)
2. **Escalado**: Las variables numéricas pueden beneficiarse de normalización
3. **Correlación**: Revisar correlación entre variables de minutos y cargos
4. **Valores Faltantes**: Verificar si existen valores nulos
5. **Desbalance de Clases**: Considerar técnicas de balanceo si es necesario

## Referencias y Fuentes

Este dataset es una versión del clásico "Churn Dataset" utilizado frecuentemente en:

- Cursos de Machine Learning y Data Science
- Competencias de análisis predictivo
- Investigación académica en customer analytics
- Benchmarking de algoritmos de clasificación

### Fuentes Alternativas de Descarga

- **Kaggle**: [Customer Churn Dataset](https://www.kaggle.com/datasets/mnassrib/telecom-churn-datasets)