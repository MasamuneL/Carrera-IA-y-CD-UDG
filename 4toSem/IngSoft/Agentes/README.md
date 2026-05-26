# Athena — Agente de búsqueda y descarga de libros

Agente ReAct que busca los 3 mejores libros/artículos sobre un tema y descarga el mejor desde Library Genesis.

## Flujo

```
tema → Tavily (top 3) → elige el mejor → verifica local → ISBN (OpenLibrary)
     → LibGen por ISBN → si falla → LibGen por título → descarga → biblioteca/
```

## Requisitos

- Python 3.10+
- Cuenta gratuita en [console.groq.com](https://console.groq.com) → API key
- Cuenta gratuita en [app.tavily.com](https://app.tavily.com) → API key

## Setup

### 1. Entrar al directorio

```bash
cd 4toSem/IngSoft/Agentes
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en esta carpeta:

```env
TAVILY_API_KEY="tu_tavily_api_key"
GROQ_API_KEY="tu_groq_api_key"
```

| Variable | Dónde obtenerla |
|---|---|
| `TAVILY_API_KEY` | [app.tavily.com](https://app.tavily.com) → API Keys |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) → API Keys |

Ambas tienen tier gratuito.

## Uso

```bash
python agent.py
```

El agente pedirá el tema:

```
¿Sobre qué tema quieres buscar un libro? → machine learning
```

El libro descargado se guarda en `biblioteca/` (creada automáticamente).

## Estructura

```
Agentes/
├── agent.py          # Agente ReAct (LangGraph + Groq llama-3.3-70b)
├── tools.py          # Tools: Tavily, OpenLibrary, LibGen, descarga
├── requirements.txt
├── .env              # No incluido en git
└── biblioteca/       # Libros descargados (no incluido en git)
```

## Notas

- LibGen utiliza el mirror `libgen.li` (accesible desde México).
- Si un mirror falla, la tool `descargar_libro` reintenta automáticamente con los siguientes.
- El agente verifica si el libro ya existe localmente antes de descargar.
