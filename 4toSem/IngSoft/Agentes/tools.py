from tavily import TavilyClient
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

load_dotenv()

LIBGEN_BASE = "https://libgen.li"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _buscar_libgen(query: str, column: str = "title") -> list:
    """Búsqueda interna en libgen.li, devuelve lista de resultados."""
    url = f"{LIBGEN_BASE}/index.php"
    params = {"req": query, "column": column, "res": 10, "sort": "year", "sortmode": "DESC"}
    resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", {"id": "tablelibgen"})
    if not table:
        return []

    resultados = []
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) < 9:
            continue

        title_text = cols[0].get_text(strip=True)
        edition_link = cols[0].find("a", href=lambda h: h and "edition.php" in h)
        direct_link = cols[6].find("a", href=lambda h: h and "file.php" in h)
        mirror_links = [a["href"] for a in cols[8].find_all("a", href=True)]

        # Priorizar ads.php (funciona sin login) sobre file.php (requiere login)
        mirrors = []
        for m in mirror_links:
            if "ads.php" in m:
                full = m if m.startswith("http") else f"{LIBGEN_BASE}{m}"
                mirrors.insert(0, full)
            elif m not in mirrors:
                mirrors.append(m if m.startswith("http") else f"{LIBGEN_BASE}{m}")

        resultados.append({
            "titulo": title_text,
            "autor": cols[1].get_text(strip=True),
            "editorial": cols[2].get_text(strip=True),
            "año": cols[3].get_text(strip=True),
            "formato": cols[7].get_text(strip=True),
            "tamaño": cols[6].get_text(strip=True).split("\n")[0].strip(),
            "mirrors": mirrors,
        })

    return resultados


@tool
def busqueda_tavily(query):
    """Busca en la web usando Tavily. Úsala para encontrar libros y artículos relevantes sobre un tema."""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query)
    return response


@tool
def buscar_y_extraer_isbn(query):
    """Busca un libro en OpenLibrary y extrae el ISBN más relevante."""
    query_clean = query.replace(" ", "+")
    ol_headers = {"User-Agent": "Athena (alan.solano6445@alumnos.udg.mx)"}

    try:
        response = requests.get(
            f"https://openlibrary.org/search.json?q={query_clean}",
            headers=ol_headers,
            timeout=15,
        )
        data = response.json()

        if data.get("numFound", 0) > 0:
            primer_libro = data["docs"][0]
            isbns = primer_libro.get("isbn", [])
            if isbns:
                isbn_13 = next((i for i in isbns if len(i) == 13), isbns[0])
                return {
                    "titulo": primer_libro.get("title"),
                    "autor": primer_libro.get("author_name", ["Desconocido"])[0],
                    "isbn": isbn_13,
                }

        return "No se encontró un ISBN válido para este tema."

    except Exception as e:
        return f"Error en la búsqueda: {str(e)}"


@tool
def obtener_enlaces_libgen(isbn: str):
    """Busca un libro en libgen.li por ISBN y devuelve los mejores 3 resultados con mirrors de descarga."""
    try:
        resultados = _buscar_libgen(isbn, column="identifier")
        if not resultados:
            return f"No se encontraron archivos en LibGen para el ISBN: {isbn}"
        return resultados[:3]
    except Exception as e:
        return f"Error al conectar con LibGen: {str(e)}"


@tool
def buscar_libgen_por_titulo(titulo: str):
    """Plan B: Busca un libro en libgen.li por título cuando la búsqueda por ISBN falla."""
    try:
        resultados = _buscar_libgen(titulo, column="title")
        if not resultados:
            return f"No se encontraron resultados por título para: {titulo}"
        return resultados[:3]
    except Exception as e:
        return f"Error en la búsqueda por título en LibGen: {str(e)}"


@tool
def descargar_libro(mirrors: list, titulo_sugerido: str, carpeta_destino: str = "biblioteca"):
    """
    Descarga un libro probando cada mirror en orden hasta que uno funcione.
    Recibe la lista 'mirrors' del resultado de búsqueda de libgen.
    El primer mirror suele ser descarga directa (libgen.li/file.php).
    """
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    nombre_limpio = "".join(c for c in titulo_sugerido if c.isalnum() or c in (" ", ".", "_")).rstrip()
    errores = []

    for mirror_url in mirrors:
        try:
            if not mirror_url.startswith("http"):
                mirror_url = f"{LIBGEN_BASE}{mirror_url}"

            sess = requests.Session()
            sess.headers.update(HEADERS)

            # Scraping del botón GET (ads.php y otros mirrors externos)
            response = sess.get(mirror_url, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            link_final = soup.find("a", string=lambda t: t and "GET" in t.upper())
            if not link_final:
                link_final = soup.select_one("#download a")
            if not link_final or not link_final.get("href"):
                errores.append(f"{mirror_url}: enlace GET no encontrado")
                continue

            href = link_final["href"]
            # Resolver URL relativa
            if href.startswith("http"):
                direct_url = href
            else:
                from urllib.parse import urljoin
                direct_url = urljoin(mirror_url, href)

            print(f"Descargando desde: {mirror_url}")
            with sess.get(direct_url, stream=True, timeout=90) as r:
                r.raise_for_status()
                content_type = r.headers.get("Content-Type", "")
                if "html" in content_type:
                    errores.append(f"{mirror_url}: respuesta HTML en lugar de archivo")
                    continue
                extension = ".epub" if "epub" in content_type or "epub" in direct_url.lower() else ".pdf"
                ruta = os.path.join(carpeta_destino, f"{nombre_limpio}{extension}")
                with open(ruta, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return f"Exito! Libro guardado en: {ruta}"

        except Exception as e:
            errores.append(f"{mirror_url}: {str(e)}")
            continue

    return "Todos los mirrors fallaron:\n" + "\n".join(errores)


@tool
def verificar_archivo_local(titulo_sugerido: str, carpeta_destino: str = "biblioteca"):
    """Verifica si un libro ya fue descargado previamente. Úsalo ANTES de intentar descargar."""
    if not os.path.exists(carpeta_destino):
        return "La carpeta no existe aún. El libro no está descargado."

    nombre_limpio = "".join(c for c in titulo_sugerido if c.isalnum() or c in (" ", ".", "_")).rstrip()
    for archivo in os.listdir(carpeta_destino):
        if nombre_limpio.lower() in archivo.lower():
            return f"El libro ya existe localmente como: {archivo}. No es necesario descargarlo."

    return "El libro no existe localmente. Procede a descargarlo."
