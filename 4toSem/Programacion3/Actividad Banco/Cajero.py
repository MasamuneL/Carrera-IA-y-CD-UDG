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

class Cajero(threading.Thread):
    def __init__(self, id, banco, status=None, **kwargs):
        super().__init__()
        self.Id = id
        self.status = status
        self.banco = banco
        self.start()
    
    def run(self):
        print(f'Cajero {self.Id} empieza operaciones...')
        time.sleep(0.02)
        self.banco.accion_cajero(self.Id)