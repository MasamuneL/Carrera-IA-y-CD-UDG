import time
from Runners import Runner
from WikiWorker import WikiWorker

print('='*50)
print('Precio de las acciones del SP500')
print('='*50)

#Creamos el objeto WikiWorker
wikiworker = WikiWorker()
wikiworker.sp500_symbols

runners_list = []

for symbol in wikiworker.sp500_symbols():
    time.sleep(0.3)
    runner=Runner(symbol)
    runners_list.append(runner)

for runner in runners_list:
    runner.join()

print('='*50)
print('Ejecucion Finalizada.')