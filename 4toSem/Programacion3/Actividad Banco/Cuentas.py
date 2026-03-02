"""
Este Programa define la Clase Cuenta.

Atributos:
1. id_cuenta = id_cliente
2. Saldo
3. Tipo de Cuenta
4. Tokken

Metodos:
1. Retiro
2. Deposito
"""
import random
import threading

class Cuenta:
    def __init__(self,id_cuenta,saldo):
        self.id_cuenta = id_cuenta
        self.saldo = saldo
        self.tipo_cuenta = random.choice(['Corriente','Ahorro','Empresarial','Jubilacion'])
        self._token = random.randint(1000,9999)
        self.lock_cuenta = threading.Lock()

    def retiro(self,monto):
        with self.lock_cuenta:
            if self.saldo >= monto:
                self.saldo -= monto
                return True
            else:
                print("Saldo insuficiente")
                return False
    
    def deposito(self,monto):
        with self.lock_cuenta:
            self.saldo += monto
            return True

    def __repr__(self):
        return f"Cuenta {self.id_cuenta} - Saldo: {self.saldo} - Tipo de Cuenta: {self.tipo_cuenta}"

        