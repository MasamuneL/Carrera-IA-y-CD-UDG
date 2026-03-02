# Dataset de Marketing Bancario Portugués

## Descripción General

Este dataset contiene datos relacionados con campañas de marketing directo de una institución bancaria portuguesa. Las campañas de marketing se basaron en llamadas telefónicas. A menudo, se requería más de un contacto con el mismo cliente para acceder si el producto (depósito a plazo bancario) sería suscrito ('yes') o no ('no').

## Información del Dataset

- **Archivo**: `banking.csv`
- **Número total de registros**: 4,119 (incluyendo header)
- **Número de características**: 21
- **Variable objetivo**: `y` (suscripción del depósito a plazo)
- **Formato**: CSV con separador punto y coma (;)
- **Codificación**: Los valores de texto están entre comillas dobles

## Distribución de la Variable Objetivo

- **Casos positivos (y = "yes")**: 451 (10.95%)
- **Casos negativos (y = "no")**: 3,668 (89.05%)

*Nota: El dataset está desbalanceado con una mayoría significativa de casos negativos.*

## Descripción de Variables

### Variables Demográficas del Cliente
1. **age**: Edad del cliente (numérica)
2. **job**: Tipo de trabajo (categórica)
   - Valores: "admin.", "blue-collar", "entrepreneur", "housemaid", "management", "retired", "self-employed", "services", "student", "technician", "unemployed", "unknown"
3. **marital**: Estado civil (categórica)
   - Valores: "divorced", "married", "single", "unknown"
4. **education**: Nivel educativo (categórica)
   - Valores: "basic.4y", "basic.6y", "basic.9y", "high.school", "illiterate", "professional.course", "university.degree", "unknown"

### Variables Financieras del Cliente
5. **default**: ¿Tiene crédito en default? (categórica: "no", "yes", "unknown")
6. **housing**: ¿Tiene préstamo hipotecario? (categórica: "no", "yes", "unknown")
7. **loan**: ¿Tiene préstamo personal? (categórica: "no", "yes", "unknown")

### Variables de la Campaña Actual
8. **contact**: Tipo de comunicación de contacto (categórica: "cellular", "telephone")
9. **month**: Último mes de contacto del año (categórica: "jan", "feb", "mar", ..., "nov", "dec")
10. **day_of_week**: Último día de contacto de la semana (categórica: "mon", "tue", "wed", "thu", "fri")
11. **duration**: Duración del último contacto en segundos (numérica)

### Variables de Campañas Anteriores
12. **campaign**: Número de contactos realizados durante esta campaña para este cliente (numérica)
13. **pdays**: Número de días que pasaron después de que el cliente fue contactado por última vez en una campaña anterior (numérica; 999 significa que el cliente no fue contactado previamente)
14. **previous**: Número de contactos realizados antes de esta campaña para este cliente (numérica)
15. **poutcome**: Resultado de la campaña de marketing anterior (categórica: "failure", "nonexistent", "success")

### Variables de Contexto Social y Económico
16. **emp.var.rate**: Tasa de variación del empleo - indicador trimestral (numérica)
17. **cons.price.idx**: Índice de precios al consumidor - indicador mensual (numérica)
18. **cons.conf.idx**: Índice de confianza del consumidor - indicador mensual (numérica)
19. **euribor3m**: Tasa Euribor a 3 meses - indicador diario (numérica)
20. **nr.employed**: Número de empleados - indicador trimestral (numérica)

### Variable Objetivo
21. **y**: ¿El cliente suscribió un depósito a plazo? (binaria: "yes", "no")


## Consideraciones para el Análisis

### Desbalance de Clases
- El dataset presenta un fuerte desbalance con aproximadamente 9:1 ratio de casos negativos a positivos
- Se recomienda usar técnicas de balanceo o métricas apropiadas para datasets desbalanceados

### Valores Faltantes
- Algunas variables contienen el valor "unknown" que representa datos faltantes
- Variables afectadas: job, marital, education, default, housing, loan

### Variables Importantes
- **duration**: Altamente correlacionada con la variable objetivo, pero no disponible antes de realizar la llamada
- **pdays**: Valor 999 indica que el cliente no fue contactado previamente
- **Variables económicas**: Proporcionan contexto temporal importante para el análisis

## Posibles Casos de Uso

1. **Clasificación binaria**: Predecir si un cliente suscribirá un depósito a plazo
2. **Análisis de segmentación**: Identificar perfiles de clientes más propensos a suscribir
3. **Optimización de campañas**: Determinar el mejor momento y método de contacto
4. **Análisis de factores económicos**: Estudiar el impacto de indicadores económicos en las decisiones de los clientes

## Enlaces y Fuentes

### Fuente Original
Este dataset es una versión del famoso "Bank Marketing Dataset" del UCI Machine Learning Repository, relacionado con campañas de marketing directo de una institución bancaria portuguesa.

### Enlaces de Descarga y Referencia

- **UCI Machine Learning Repository**: [Bank Marketing Dataset](https://archive.ics.uci.edu/ml/datasets/Bank+Marketing)
- **Kaggle**: [Bank Marketing Dataset](https://www.kaggle.com/datasets/henriqueyamahata/bank-marketing)
- **OpenML**: [Bank Marketing Dataset](https://www.openml.org/d/1461)

### Publicación Académica Original
- **Título**: "A Data-Driven Approach to Predict the Success of Bank Telemarketing"
- **Autores**: S. Moro, P. Cortez, P. Rita
- **Revista**: Decision Support Systems, Elsevier, 62:22-31, June 2014
- **DOI**: [10.1016/j.dss.2014.03.001](https://doi.org/10.1016/j.dss.2014.03.001)