from tavily import TavilyClient
import os
from dotenv import load_dotenv
import json
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from libgen_api import LibgenSearch

load_dotenv()

@tool
def busqueda_tavily(query):
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query)
    return response

@tool
def buscar_y_extraer_isbn(query):
    """
    Busca un libro en OpenLibrary y extrae el ISBN más relevante.
    """
    query_clean = query.replace(" ", "+")
    headers = {"User-Agent": "Athena (alan.solano6445@alumnos.udg.mx)"}
    
    try:
        response = requests.get(f'https://openlibrary.org/search.json?q={query_clean}', headers=headers)
        data = response.json()
        
        # 1. Verificar si hay resultados
        if data.get("numFound", 0) > 0:
            # Tomamos el primer libro (el más relevante)
            primer_libro = data["docs"][0]
            
            # 2. Intentar extraer la lista de ISBNs
            isbns = primer_libro.get("isbn", [])
            
            if isbns:
                # 3. Preferir ISBN de 13 dígitos (empiezan con 978)
                isbn_13 = next((i for i in isbns if len(i) == 13), isbns[0])
                return {
                    "titulo": primer_libro.get("title"),
                    "autor": primer_libro.get("author_name", ["Desconocido"])[0],
                    "isbn": isbn_13
                }
        
        return "No se encontró un ISBN válido para este tema."
    
    except Exception as e:
        return f"Error en la búsqueda: {str(e)}"

@tool
def obtener_enlaces_libgen(isbn: str):
    """
    Busca un libro en Library Genesis usando su ISBN y devuelve los 
    enlaces de descarga de los mejores 3 resultados.
    """
    s = LibgenSearch()
    
    try:
        # 1. Realizar la búsqueda por ISBN
        # El ISBN debe ser un string sin guiones
        resultados = s.search_isbn(isbn)
        
        if not resultados:
            return f"No se encontraron archivos en LibGen para el ISBN: {isbn}"

        # 2. Seleccionar los mejores (máximo 3)
        # Aquí podrías añadir lógica extra, como preferir 'pdf' o 'epub'
        mejores_resultados = resultados[:3]
        
        biblioteca_links = []
        
        for libro in mejores_resultados:
            # Extraemos la información clave para el agente
            info = {
                "titulo": libro.get("Title"),
                "autor": libro.get("Author"),
                "formato": libro.get("Extension"),
                "tamaño": libro.get("Size"),
                "link_descarga": libro.get("Mirror_1") # Usualmente el mirror principal
            }
            biblioteca_links.append(info)
            
        return biblioteca_links

    except Exception as e:
        return f"Error al conectar con LibGen: {str(e)}"
    
@tool
def descargar_libro(mirror_url: str, titulo_sugerido: str, carpeta_destino: str = "biblioteca"):
    """
    Navega al mirror de LibGen, encuentra el enlace de descarga real 
    y guarda el libro en una carpeta local.
    """
    try:
        # 1. Crear carpeta si no existe
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        # 2. Entrar a la página del mirror (ej. library.lol)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(mirror_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Buscar el enlace que dice "GET" (es el estándar de LibGen)
        link_final = soup.find('a', string=lambda t: t and 'GET' in t.upper())
        if not link_final:
            # Intento alternativo por si cambió el diseño
            link_final = soup.select_one('#download a') 
            
        if not link_final or not link_final.get('href'):
            return "No se pudo encontrar el enlace de descarga directa en el mirror."

        direct_url = link_final['href']

        # 4. Limpiar el nombre del archivo
        # Quitamos caracteres prohibidos en nombres de archivos
        nombre_limpio = "".join(c for c in titulo_sugerido if c.isalnum() or c in (' ', '.', '_')).rstrip()
        
        # Determinar extensión (si el mirror nos dice que es pdf o epub)
        extension = ".pdf" # Default
        if "epub" in mirror_url.lower() or "epub" in direct_url.lower():
            extension = ".epub"
            
        ruta_archivo = os.path.join(carpeta_destino, f"{nombre_limpio}{extension}")

        # 5. Descargar el archivo en "streams" (pedazos) para no saturar la RAM
        print(f"Descargando: {titulo_sugerido}...")
        with requests.get(direct_url, stream=True, headers=headers) as r:
            r.raise_for_status()
            with open(ruta_archivo, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return f"¡Éxito! Libro guardado en: {ruta_archivo}"

    except Exception as e:
        return f"Error durante la descarga: {str(e)}"
    
@tool
def buscar_libgen_por_titulo(titulo: str):
    """
    Plan B: Busca un libro en LibGen por su título cuando la búsqueda por ISBN falla.
    """
    s = LibgenSearch()
    try:
        # Buscamos por título
        resultados = s.search_title(titulo)
        
        if not resultados:
            return f"No se encontraron resultados por título para: {titulo}"
            
        mejores_resultados = resultados[:3]
        biblioteca_links = []
        
        for libro in mejores_resultados:
            info = {
                "titulo": libro.get("Title"),
                "autor": libro.get("Author"),
                "formato": libro.get("Extension"),
                "tamaño": libro.get("Size"),
                "link_descarga": libro.get("Mirror_1")
            }
            biblioteca_links.append(info)
            
        return biblioteca_links
    except Exception as e:
        return f"Error en la búsqueda por título en LibGen: {str(e)}"
    
@tool
def verificar_archivo_local(titulo_sugerido: str, carpeta_destino: str = "biblioteca"):
    """
    Verifica si un libro ya fue descargado previamente en la carpeta local.
    Úsalo ANTES de intentar descargar un libro.
    """
    if not os.path.exists(carpeta_destino):
        return "La carpeta no existe aún. El libro no está descargado."
        
    nombre_limpio = "".join(c for c in titulo_sugerido if c.isalnum() or c in (' ', '.', '_')).rstrip()
    
    # Revisamos si existe el archivo en pdf o epub
    archivos_existentes = os.listdir(carpeta_destino)
    for archivo in archivos_existentes:
        if nombre_limpio.lower() in archivo.lower():
            return f"¡El libro ya existe localmente como: {archivo}! No es necesario descargarlo de nuevo."
            
    return "El libro no existe localmente. Procede a descargarlo."