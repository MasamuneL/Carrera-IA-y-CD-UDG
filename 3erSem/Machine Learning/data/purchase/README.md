# Dataset: Compras por Género (Gender Purchase Dataset)

## Descripción

Este dataset contiene información sobre el comportamiento de compra de clientes segmentado por género. Es un dataset simple y efectivo para el análisis de probabilidades, especialmente útil para estudios de inferencia bayesiana, tablas de contingencia y probabilidades condicionales.

## Estructura del Dataset

**Archivo:** `gender_purrchase.csv`

### Variables

| Variable | Tipo | Descripción | Valores Posibles |
|----------|------|-------------|------------------|
| `Gender` | Categórica | Género del cliente | `Female`, `Male` |
| `Purchase` | Categórica | Decisión de compra | `Yes`, `No` |

### Características del Dataset

- **Total de observaciones:** 511 registros (sin contar el header)
- **Variables:** 2 variables categóricas
- **Formato:** CSV con separador de coma
- **Encoding:** UTF-8
- **Missing values:** No hay valores faltantes

## Distribución de los Datos

### Por Género
- **Female:** 265 registros (51.9%)
- **Male:** 246 registros (48.1%)

### Por Decisión de Compra
- **Yes (Compra):** 280 registros (54.8%)
- **No (No compra):** 231 registros (45.2%)

### Tabla de Contingencia

|        | No Compra | Sí Compra | Total |
|--------|-----------|-----------|-------|
| Female | 106 (20.7%) | 159 (31.1%) | 265 |
| Male   | 125 (24.5%) | 121 (23.7%) | 246 |
| **Total** | **231** | **280** | **511** |

## Probabilidades Clave

### Probabilidades Marginales
- P(Female) = 265/511 ≈ 0.519
- P(Male) = 246/511 ≈ 0.481
- P(Purchase = Yes) = 280/511 ≈ 0.548
- P(Purchase = No) = 231/511 ≈ 0.452

### Probabilidades Condicionales
- P(Purchase = Yes | Female) = 159/265 ≈ 0.600
- P(Purchase = Yes | Male) = 121/246 ≈ 0.492
- P(Female | Purchase = Yes) = 159/280 ≈ 0.568
- P(Male | Purchase = Yes) = 121/280 ≈ 0.432

## Aplicaciones Educativas

Este dataset es ideal para:

### 1. **Tablas de Contingencia**
- Análisis de frecuencias cruzadas
- Cálculo de frecuencias relativas
- Interpretación de asociaciones entre variables

### 2. **Probabilidades Condicionales**
- Cálculo de P(A|B) y P(B|A)
- Aplicación del Teorema de Bayes
- Análisis de independencia estadística

### 3. **Diagramas de Árbol**
- Representación visual de probabilidades
- Cálculo de probabilidades conjuntas
- Análisis de escenarios secuenciales

### 4. **Inferencia Bayesiana**
- Actualización de creencias
- Cálculo de probabilidades posteriores
- Análisis de hipótesis

### 5. **Tests de Independencia**
- Chi-cuadrado de Pearson
- Test exacto de Fisher
- Análisis de asociación

## Insights del Dataset

1. **Diferencia de género en compras:** Las mujeres muestran una mayor propensión a comprar (60.0%) comparado con los hombres (49.2%).

2. **Distribución equilibrada:** El dataset tiene una distribución relativamente equilibrada tanto en género como en decisiones de compra.

3. **Tamaño adecuado:** Con 511 observaciones, el dataset es suficientemente grande para análisis estadísticos básicos pero manejable para fines educativos.
