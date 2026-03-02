# Company ABC Profit Dataset

## Descripción

Este dataset contiene datos históricos de ganancias de una compañía ABC durante un período de 200 años, desde 1821 hasta 2020. Los datos representan una serie temporal de las ganancias anuales de la empresa, expresadas en miles de rupias (Rs '000).

## Estructura del Dataset

### Archivo: `CompanyABCProfit.csv`

**Formato:** CSV (Comma Separated Values)  
**Tamaño:** 201 filas (incluyendo header)  
**Período:** 1821 - 2020 (200 años de datos)

### Columnas

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `Year` | Integer | Año del registro (1821-2020) |
| `Profit(Rs '000)` | Integer | Ganancia anual en miles de rupias |

### Características de los Datos

- **Rango temporal:** 200 años consecutivos (1821-2020)
- **Frecuencia:** Anual
- **Unidad monetaria:** Miles de rupias (Rs '000)
- **Valores negativos:** Sí (indica pérdidas en algunos años)
- **Datos faltantes:** No se observan valores faltantes

## Estadísticas Básicas

- **Número total de observaciones:** 200
- **Rango de años:** 1821-2020
- **Valores de ganancia:** Incluye tanto ganancias positivas como pérdidas negativas
- **Ejemplo de pérdida:** -178 (miles de Rs) en 2018

## Casos de Uso

Este dataset es ideal para:

1. **Análisis de series temporales**
   - Modelado de tendencias a largo plazo
   - Análisis de estacionalidad y ciclos económicos
   - Predicción de ganancias futuras
   - Pruebas de normalidad

2. **Machine Learning**
   - Modelos de regresión temporal
   - Modelos ARIMA

3. **Inferencia Bayesiana**
   - Modelado probabilístico de ganancias
   - Estimación de parámetros con incertidumbre
   - Predicción con intervalos de credibilidad

4. **Análisis estadístico**
   - Detección de outliers
   - Análisis de volatilidad
   - Estudios de correlación temporal

## Consideraciones

- Los datos históricos de 200 años pueden incluir efectos de inflación no ajustados
- El dataset es sintético y puede haber sido generado para propósitos educativos