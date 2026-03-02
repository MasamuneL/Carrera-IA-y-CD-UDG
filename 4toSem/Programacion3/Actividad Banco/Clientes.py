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
import random

#import Banco

class Usuario(threading.Thread):
    def __init__(self, id_cliente, banco, **kwargs):
        super().__init__() #llamamos al constructor de la clase padre
        self.Id = id_cliente
        self.banco = banco
        self.actlist = ["Retirar","Depositar","Consultar","Transferir","BorrarUsuario"]
        self.start() #inicia el hilo
    
    def run(self):
        print(f'Cliente {self.Id} llego al banco...')
        time.sleep(0.02)
        self.banco.accion_cliente(self.Id)