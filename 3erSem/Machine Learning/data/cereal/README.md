# Dataset de Cereales para el Desayuno

## Descripción General

Este dataset contiene información nutricional y características de 77 cereales para el desayuno diferentes. Es ampliamente utilizado en análisis de datos, machine learning y estadística para explorar relaciones entre variables nutricionales y ratings de cereales.

## Información del Dataset

- **Número de registros**: 77 cereales
- **Número de variables**: 16 columnas
- **Formato**: CSV (Comma Separated Values)
- **Tamaño del archivo**: ~5KB

## Variables del Dataset

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `name` | String | Nombre del cereal |
| `mfr` | Categórica | Fabricante (A=American Home Food Products, G=General Mills, K=Kelloggs, N=Nabisco, P=Post, Q=Quaker Oats, R=Ralston Purina) |
| `type` | Categórica | Tipo de cereal (C=Cold, H=Hot) |
| `calories` | Numérica | Calorías por porción |
| `protein` | Numérica | Gramos de proteína |
| `fat` | Numérica | Gramos de grasa |
| `sodium` | Numérica | Miligramos de sodio |
| `fiber` | Numérica | Gramos de fibra dietética |
| `carbo` | Numérica | Gramos de carbohidratos complejos |
| `sugars` | Numérica | Gramos de azúcares |
| `potass` | Numérica | Miligramos de potasio |
| `vitamins` | Numérica | Vitaminas y minerales (0, 25, o 100, indicando el porcentaje del FDA) |
| `shelf` | Numérica | Posición en el estante de exhibición (1, 2, o 3, contando desde el suelo) |
| `weight` | Numérica | Peso en onzas de una porción |
| `cups` | Numérica | Número de tazas en una porción |
| `rating` | Numérica | Rating de calidad nutricional calculado por Consumer Reports |

## Fabricantes Incluidos

- **American Home Food Products** (A)
- **General Mills** (G) - Cheerios, Cocoa Puffs, etc.
- **Kelloggs** (K) - Corn Flakes, All-Bran, etc.
- **Nabisco** (N)
- **Post** (P)
- **Quaker Oats** (Q)
- **Ralston Purina** (R)

## Casos de Uso Comunes

1. **Análisis Exploratorio de Datos**: Explorar distribuciones y correlaciones entre variables nutricionales
2. **Regresión**: Predecir el rating basado en características nutricionales
3. **Clasificación**: Clasificar cereales por tipo, fabricante o nivel de salubridad
4. **Clustering**: Agrupar cereales similares basándose en su perfil nutricional
5. **Visualización de Datos**: Crear gráficos para entender patrones nutricionales

## Ejemplos de Análisis Posibles

- Relación entre contenido de azúcar y rating
- Comparación nutricional entre fabricantes
- Análisis de la posición en estante vs. características nutricionales
- Identificación de cereales más saludables basándose en múltiples criterios
- Análisis de correlación entre fibra, proteína y rating

## Notas Importantes

- Los valores de potasio con -1 indican datos faltantes
- El rating es una medida compuesta que considera múltiples factores nutricionales
- Todos los valores nutricionales están normalizados por porción estándar
- La mayoría de cereales son fríos (Cold), con pocos cereales calientes (Hot)

## Fuente y Referencias

**Fuente Original**: Este dataset proviene de la revista Consumer Reports (1999) y ha sido ampliamente distribuido para propósitos educativos.

**Fuente en Kaggle**: 
- [80 Cereals Dataset](https://www.kaggle.com/datasets/crawford/80-cereals)


