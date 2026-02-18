"""
Este programa contiene la clase Banquero - Hilos Consumidores

Atributos:
1. id_banquero
2. Nombre
3. Estatus

Funciones:
1. Mostrar Saldo
2. Dar dinero a cliente - Cuenta
3. Recibir dinero a cliente - cuneta
4. Procesar tansferencia
"""

import threading
import time

class cajero(threading.Thread):
    def __init__(self, id, nombre, status, **kwargs):
        super().__init__()
        self.Id = id
        self.name = nombre
        self.status = status
        self.start()
    
    def run(self):
        print(f'Hilo Cajero {self.Id} ejecutandose ...')