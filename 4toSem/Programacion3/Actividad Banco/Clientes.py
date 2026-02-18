"""
Este Programa va a definir la clase clientes, los cuales seran hilos Productores.

Atributos:
1. Id_cliente

FUNCIONES (Banco):
1. Consultar saldo
2. Transferir
3. Retirar dinero - Cuenta
4. Depositar Dinero - Cuenta
"""

import threading
import time

#import Banco

class usuario(threading.Thread):
    def __init__(self, id_cliente, **kwargs):
        super().__init__() #llamamos al constructor de la clase padre
        self.Id = id_cliente
        #self.start() #inicia el hilo
    
    def run(self):
        print(f'Hilo Clinte {self.Id} Ejecutandose...')