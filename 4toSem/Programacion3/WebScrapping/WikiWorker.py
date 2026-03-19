import requests
from bs4 import BeautifulSoup
import time
import os

os.system('clear')

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
            symbol = row.find('td').text.strip()
            yield symbol # Regresa elemento por elemento
    
    def sp500_symbols(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:147.0) Gecko/20100101 Firefox/147.0'}
        answer = requests.get(self._url, headers=headers)
        if answer.status_code != 200:
            print("Couldn't obtain an answer")
            return
        htmlpage = answer.text
        yield from self.extract_symbols(htmlpage)




# wiki = WikiWorker()
# for symbol in wiki.sp500_symbols():
#     print(symbol)