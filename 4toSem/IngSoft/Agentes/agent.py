import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

from tools import (
    busqueda_tavily,
    buscar_y_extraer_isbn,
    obtener_enlaces_libgen,
    descargar_libro,
    buscar_libgen_por_titulo,
    verificar_archivo_local,
)

load_dotenv()

TOOLS = [
    busqueda_tavily,
    buscar_y_extraer_isbn,
    obtener_enlaces_libgen,
    buscar_libgen_por_titulo,
    verificar_archivo_local,
    descargar_libro,
]

SYSTEM_PROMPT = """Eres Athena, un agente especializado en encontrar y descargar los mejores recursos académicos.

Cuando el usuario te dé un tema, sigue este flujo estrictamente:

1. **BUSCAR** - Usa `busqueda_tavily` con una query como "best books on [tema]" o "mejores libros sobre [tema]".
   Analiza los resultados e identifica los 3 mejores libros o artículos más relevantes y académicos.
   Preséntale al usuario los 3 candidatos con título, autor y por qué son relevantes.

2. **SELECCIONAR** - Elige el MEJOR de los 3 (el más completo, más citado, o más apropiado para el tema).

3. **VERIFICAR LOCAL** - Usa `verificar_archivo_local` con el título del libro seleccionado.
   Si ya existe localmente, informa al usuario y termina.

4. **OBTENER ISBN** - Usa `buscar_y_extraer_isbn` con el título del libro.
   Si no encuentra ISBN, ve al Plan B.

5. **BUSCAR EN LIBGEN** (Plan A) - Usa `obtener_enlaces_libgen` con el ISBN obtenido.
   Si no hay resultados, ve al Plan B.

   **Plan B** - Usa `buscar_libgen_por_titulo` con el título del libro.

6. **DESCARGAR** - Usa `descargar_libro` pasando el campo `mirrors` (lista completa) del primer
   resultado de LibGen y el título del libro. La tool reintenta automáticamente cada mirror.
   La carpeta destino por defecto es "biblioteca".

7. **REPORTAR** - Informa al usuario el resultado final: qué se descargó y dónde está guardado.

IMPORTANTE:
- Siempre verifica localmente ANTES de descargar.
- Si el Plan A (ISBN) falla, usa Plan B (búsqueda por título) sin preguntarle al usuario.
- Pasa SIEMPRE la lista completa de mirrors a `descargar_libro`, nunca solo uno.
- Responde siempre en español.
"""

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)

agent = create_react_agent(
    model=llm,
    tools=TOOLS,
    prompt=SYSTEM_PROMPT,
)


def run(tema: str):
    print(f"\nBuscando recursos sobre: {tema}\n{'=' * 50}")
    result = agent.invoke({"messages": [("human", tema)]})
    respuesta = result["messages"][-1].content
    print(respuesta)
    return respuesta


if __name__ == "__main__":
    tema = input("¿Sobre qué tema quieres buscar un libro? → ")
    run(tema)
