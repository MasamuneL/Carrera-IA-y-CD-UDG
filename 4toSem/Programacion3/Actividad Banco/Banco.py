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
        self.banco_abierto = True
        
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
            self.timbre.notify_all()

    def accion_cajero(self,id_cajero):
        # Acciones Cajero V2
        # 0. Comprobar si hay elementos en la fila
        while self.banco_abierto or len(self.fila_transacciones) > 0:
            with self.timbre:
                while len(self.fila_transacciones) == 0 and self.banco_abierto:
                    print(f"Cajero {id_cajero} esperando transaccion...")
                    self.timbre.wait()
                # Si el banco cerro y la fila quedo vacia, salimos
                if len(self.fila_transacciones) == 0:
                    break
                # 1. Ver la fila y checar la transaccion proxima
                tx = self.fila_transacciones.pop(0)  # extrae y quita el elemento transaccion 0 'el primero en la fila' de la fila
                # 2. Checar tipo de transaccion
                tipo = tx.tipo_transaccion
                # 3. Procesar la transaccion
                # Hacemos unos 'if/elif' para distinguir los tipos y definir las acciones
                if tipo == 'Retiro':
                    if self.boveda >= tx.monto: #Checa si hay dinero suficiente en la boveda
                        if self.userlist[tx.cuenta_origen].retiro(tx.monto): #Retorna True si se retiro (se ejecuta) y False si no se retiro (no se ejecuta)
                            with self.lock_boveda: #Bloquea la boveda para que solo un cajero pueda acceder a ella
                                self.boveda -= tx.monto #Resta el monto de la boveda
                                print(f"Cajero {id_cajero} retiro {tx.monto} de la cuenta {tx.cuenta_origen}")
                    else:
                        print(f"Cajero {id_cajero} no puede retirar {tx.monto} de la cuenta {tx.cuenta_origen} por falta de dinero en la boveda.")
                elif tipo == 'Deposito':
                    self.userlist[tx.cuenta_origen].deposito(tx.monto)
                    with self.lock_boveda:
                        self.boveda += tx.monto
                    print(f"Cajero {id_cajero} deposito {tx.monto} en la cuenta {tx.cuenta_origen}")
                elif tipo == 'Consulta de saldo':
                    print(f"Cajero {id_cajero} consulto el saldo de la cuenta {tx.cuenta_origen}")
                    print(self.userlist[tx.cuenta_origen])
                elif tipo == 'Transferencia':
                    if self.userlist[tx.cuenta_origen].retiro(tx.monto):
                        self.userlist[tx.cuenta_destino].deposito(tx.monto)
                        print(f"Cajero {id_cajero} transferio {tx.monto} de la cuenta {tx.cuenta_origen} a la cuenta {tx.cuenta_destino}")
                    else:
                        print(f"Cajero {id_cajero} no puede transferir {tx.monto} de la cuenta {tx.cuenta_origen} a la cuenta {tx.cuenta_destino} por falta de dinero en la cuenta de origen.")
                else:
                    print('No se pudo processar la transaccion (no valida) ...')
                    return
                # 4. Avisar al cliente que la transaccion se completo
                self.timbre.notify_all()

        
        
    
    def borrarusuario(self, usuario):
        """
        Permite eliminar un usuario del banco.
        Actualiza los totales del banco y cajero.

        Args:
            usuario: El objeto del usuario que se eliminará.

        Returns:
            bool: True si la operación se realizó con éxito.
        """
        with self.timbre:
            if usuario in self.userlist:
                self.userlist.remove(usuario)
                with self.lock_boveda:
                    self.boveda -= usuario.saldo
                return True
        return False
    
"""# Acciones del cajero
        # 0. Esperar a que haya una transaccion en la fila
        with self.timbre:
            while len(self.fila_transacciones) == 0:
                print(f"Cajero {id_cajero} esperando transaccion...")
                self.timbre.wait()
        # 1. Tomar la transaccion de la fila
        tx = self.fila_transacciones.pop(0)
        # 2. Procesar la transaccion
        match tx.tipo_transaccion:
            case "Retiro":
                if self.userlist[tx.cuenta_origen].retiro(tx.monto):
                    with self.lock_boveda:
                        self.boveda -= tx.monto
                        print(f"Cajero {id_cajero} retiro {tx.monto} de la cuenta {tx.cuenta_origen}")
            case "Deposito":
                if self.userlist[tx.cuenta_origen].deposito(tx.monto):
                    with self.lock_boveda:
                        self.boveda += tx.monto
                        print(f"Cajero {id_cajero} deposito {tx.monto} en la cuenta {tx.cuenta_origen}")
            case "Consulta de saldo":
                print(f"Cajero {id_cajero} consulto el saldo de la cuenta {tx.cuenta_origen}")
            case "Transferencia":
                if self.userlist[tx.cuenta_origen].retiro(tx.monto):
                    self.userlist[tx.cuenta_destino].deposito(tx.monto)
                    print(f"Cajero {id_cajero} transfirio {tx.monto} de la cuenta {tx.cuenta_origen} a la cuenta {tx.cuenta_destino}")
            case _:
                print("Opcion de operacion no valida")
        # 3. Notificar al cliente que la transaccion fue procesada
        self.timbre.notify_all()"""

