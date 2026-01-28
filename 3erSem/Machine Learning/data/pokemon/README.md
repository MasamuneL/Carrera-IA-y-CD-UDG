# Dataset de Pokémon

## Descripción General

Este directorio contiene un dataset público con información sobre Pokémon, incluyendo sus nombres y tipos. El dataset está diseñado para ser utilizado en proyectos de Machine Learning e Inferencia Bayesiana.

## Archivos

### `pokemon.csv`
- **Tamaño**: 21 KB
- **Registros**: 1,009 Pokémon (1,010 líneas incluyendo el header)
- **Formato**: CSV (Comma Separated Values)
- **Codificación**: UTF-8

## Estructura de los Datos

El archivo CSV contiene las siguientes columnas:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `Name` | String | Nombre del Pokémon |
| `Type` | String | Tipo(s) del Pokémon, separados por coma si tiene múltiples tipos |

### Ejemplos de Registros

```csv
Name,Type
Bulbasaur,"Grass, Poison"
Charmander,Fire
Charizard,"Fire, Flying"
Squirtle,Water
Pikachu,Electric
```

## Casos de Uso

Este dataset es ideal para:

1. **Análisis exploratorio de datos**
   - Distribución de tipos de Pokémon
   - Análisis de frecuencia de combinaciones de tipos

## Notas Técnicas

- Los nombres de Pokémon mantienen su formato original (incluyendo caracteres especiales y guiones)
- Los tipos están en inglés
- Algunos Pokémon tienen formas especiales o regionales que pueden aparecer como entradas separadas
- El dataset incluye Pokémon legendarios y míticos

## Fuente y Actualización

- **Última actualización**: Febrero 2024
- El dataset incluye Pokémon hasta la 9ª generación (Paldea)
- Incluye formas especiales como "Walking Wake" e "Iron Leaves"
