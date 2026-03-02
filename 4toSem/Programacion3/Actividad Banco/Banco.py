"""
Aqui definiremos la clase banco clase Banco

Atributos:
1. Boveda (Dinero total)
2. Nombre del Banco
3. Condition Variable - timbre
4. Cuentas de los Usuarios
5. Cantidad de cajeros

Metodos:
1. Acciones Cliente

2. Acciones Cajero

"""
import threading
import random
import time
from Cuentas import Cuenta
from Transacciones import Transaccion

class Banco:
    def __init__(self, nombre, d_inicial, num_clientes, num_cajeros):
        self.name = nombre
        self.boveda = d_inicial
        self.lock_boveda = threading.Lock()
        
        #para hacer una fila de transacciones
        self.timbre = threading.Condition() #avisar entre clientes y cajeros
        self.fila_transacciones = []
        self.capacidad_fila = num_cajeros
        #crear las cuentas de los clientes
        self.userlist = [Cuenta(i,random.uniform(400,10000)) for i in range(num_clientes)]
        self.num_cajeros = num_cajeros

    def accion_cliente(self,id_cliente):
        #acciones del cliente
        #0. Revisa si hay lugar en la fila para formarse (fila, condition variable)
        with self.timbre:
            while len(self.fila_transacciones) >= self.capacidad_fila:
                print(f"Fila llena, cliente {id_cliente} espera por su turno...")
                self.timbre.wait()
        #1. Generar la solicitud de una accion
            #Para saber la transacion necesitamos saber el tipo, monto, cuneta origen etc.
            eleccion = random.choice(['Retiro','Deposito','Consulta de saldo','Transferencia'])
            match eleccion:
                case "Retiro":
                    monto = random.uniform(100,1000)
                    #Creamos el objeto transaccion
                    tx = Transaccion(tipo_transaccion=eleccion,cuenta_origen=id_cliente,monto=monto)
                    #2. Agregar la transaccion a la fila
                    self.fila_transacciones.append(tx)

                case "Deposito":
                    monto = random.uniform(100,1000)
                    #Creamos el objeto transaccion
                    tx = Transaccion(tipo_transaccion=eleccion,cuenta_origen=id_cliente,monto=monto)
                    #2. Agregar la transaccion a la fila
                    self.fila_transacciones.append(tx)

                case "Consulta de saldo":
                    tx = Transaccion(tipo_transaccion=eleccion,cuenta_origen=id_cliente)
                    #2. Agregar la transaccion a la fila
                    self.fila_transacciones.append(tx)

                case "Transferencia":
                    monto = random.uniform(100,1000)
                    cuenta_destino = None
                    while cuenta_destino == id_cliente or cuenta_destino == None:
                        cuenta_destino = random.randint(0,len(self.userlist)-1)
                    #Creamos el objeto transaccion
                    tx = Transaccion(tipo_transaccion=eleccion,cuenta_origen=id_cliente,monto=monto,cuenta_destino=cuenta_destino)
                    #2. Agregar la transaccion a la fila
                    self.fila_transacciones.append(tx)
                case _:
                    print("Opcion de operacion no valida")
                    return
        #3. Avisar al cajero que agrego una solicitud a la fila
            self.timbre.notifyAll()

    def accion_cajero(self,id_cajero):
        pass
    
    def borrarusuario(self,usuario):
        """
        Permite eliminar un usuario del banco.
        Actualiza los totales del banco y cajero.

        Args:
            usuario: El objeto del usuario que se eliminará.

        Returns:
            bool: True si la operación se realizó con éxito.
        """
        self.userlist.remove(usuario)
        self.boveda -= usuario.saldo
        return True
    