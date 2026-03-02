"""
En este programa se define la clase Transacciones la cual generara objetos de este mismo tipo

Atributos:
1. Cuenta origen
2. Cuenta destino
3. Monto
4. Tipo de transaccion
5. Id_transaccion

Acciones:
1. imprimir un reporte de la transaccion
"""
import threading

class Transaccion:
    #contador global para generar id
    #Cuando hay un "_" al inicio de una variable, significa que es privada
    _contador = 0
    _lock_contador = threading.Lock()
    def __init__(self,tipo_transaccion,cuenta_origen,monto=0,cuenta_destino=None):
        with Transaccion._lock_contador:
            Transaccion._contador += 1
            self.id_transaccion = Transaccion._contador
        self.cuenta_origen = cuenta_origen
        self.cuenta_destino = cuenta_destino
        self.monto = monto
        self.tipo_transaccion = tipo_transaccion

    def __repr__(self):
        return f"Reporte de Transaccion\nTipo de Transaccion: {self.tipo_transaccion}\nId de Transaccion: {self.id_transaccion}\nCuenta Origen: {self.cuenta_origen}\nCuenta Destino: {self.cuenta_destino}\nMonto: {self.monto}\n"
    
