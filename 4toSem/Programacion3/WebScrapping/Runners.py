import threading 
import requests
import time
from lxml import html
from requests.exceptions import ContentDecodingError, RequestException
from RotatingUserAgents import get_random_user_agent

class Runner(threading.Thread):

    def __init__(self, symbol):
        super().__init__()
        self._url = "https://finance.yahoo.com/quote/"
        self._xpath = '//*[@id="main-content-wrapper"]/section[1]/div[2]/div[1]/section/div/section/div[1]/span[1]'
        self._symbol = symbol
        self.start()

    def run(self):
        try:
            # Llamamos a la funcion para tener user agents aleatorios
            agent = get_random_user_agent()
            headers = {'User-Agent': get_random_user_agent()}
            new_url = self._url+self._symbol
            answer = requests.get(new_url, headers=headers)
            if answer.status_code != 200:
                print(f"Couldn't obtain an answer. Status code: {answer.status_code}")
                return
            htmlpage = answer.text
            page = html.fromstring(htmlpage)
            price = float(page.xpath(self._xpath)[0].text.replace(",","").strip())
            print(f'the symbol {self._symbol} is currently at: {price} $')
        except ContentDecodingError as e:
            print(f'Decodification error  gzip:', e)
            print('Agent:', agent)
            return
        except RequestException as e:
            print(f'Error at {new_url}: {e}')
            return

   

    # def yq_symbol(self):
    #     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:147.0) Gecko/20100101 Firefox/147.0'}
    #     new_url = self._url+self._symbol
    #     answer = requests.get(new_url, headers=headers)
    #     if answer.status_code != 200:
    #         print("Couldn't obtain an answer")
    #         return
    #     htmlpage = answer.text
    #     return self.extract_price(htmlpage, self._xpath)

# hilo = Runner('NVDA')
# hilo.join()
# print('Ejecuscion Finalizada')

    
