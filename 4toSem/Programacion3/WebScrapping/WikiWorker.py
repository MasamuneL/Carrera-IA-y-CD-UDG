import requests
from bs4 import BeautifulSoup
import time

class WikiWorker:
    def __init__(self):
        self._url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
    @staticmethod
    def extract_symbols(pagina_html):
        soup = BeautifulSoup(pagina_html, 'lxml')
        #extraemos la tabla del html
        table = soup.find(id='constituents')
        #Para evitar errores
        if not table:
            print('Table not found')
            return
        # Definimos una lista con todas las filas de la tabla
        table_rows = table.find_all('tr')
        # Definimos un ciclo para agregar los simbolos a la lista
        for row in table_rows[1:]:
            symbol = row.find('td').text.strip('\n')
            yield symbol



wiki = WikiWorker()
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(wiki._url, headers=headers)
print(r.text)