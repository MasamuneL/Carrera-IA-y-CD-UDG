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
import time
import threading

class Banco:
    def __init__(self, nombre, d_inicial):
        self.name = nombre
        self.boveda = d_inicial
        self.timbre = threading.Condition()
        self.userlist = []

    def accion_cliente(self):
        print("Cliente haciendo Solicitud...")
        time.sleep(2)
        print("Cliente finalizo solicitud.")

    def accion_cajero(self):
        print("Cajero procesando Solicitud...")
        time.sleep(2)
        print("Cajero proceso la Solicitud .")

    def crearcajero(self,cajero):
        """
        Permite crear un cajero en el banco.
        Agrega el cajero a la lista de cajeros y actualiza los totales del banco y cajero.

        Args:
            cajero: El objeto del cajero que se creará.

        Returns:
            bool: True si la operación se realizó con éxito.
        """
        self.cajerolist.append(cajero)
        
    def crearusuario(self,usuario):
        """
        Permite crear un usuario en el banco.
        Agrega el usuario a la lista de usuarios y actualiza los totales del banco y cajero.

        Args:
            usuario: El objeto del usuario que se creará.

        Returns:
            bool: True si la operación se realizó con éxito.
        """
        self.userlist.append(usuario)
        
    def retirar(self,usuario,monto):
        """
        Permite retirar dinero de una cuenta.
        Actualiza el saldo del usuario y los totales del banco y cajero.

        Args:
            usuario: El objeto del usuario que realiza el retiro.
            monto: La cantidad de dinero a retirar.

        Returns:
            bool: True si la operación se realizó con éxito.
        """
        if usuario.saldo >= monto:
            usuario.saldo -= monto
            self.boveda -= monto
            self.dinerocajero -= monto
            return True
        else:
            return False
    
    def depositar(self,usuario,monto):
        """
        Permite realizar un depósito a la cuenta de un usuario.
        Actualiza el saldo del usuario y los totales del banco y cajero.

        Args:
            usuario: El objeto del usuario que realiza el depósito.
            monto: La cantidad de dinero a depositar.

        Returns:
            bool: True si la operación se realizó con éxito.
        """
        usuario.saldo += monto
        self.dinerototal += monto
        self.dinerocajero += monto
        return True

    def consultar(self,usuario):
        """
        Permite consultar el saldo de la cuenta de un usuario.
        Muesta el saldo actualizado.

        Args:
            usuario: El objeto del usuario que consulta el saldo.

        Returns:
            float: Saldo de la cuenta del usuario.
        """
        return usuario.saldo
    
    def transferir(self,usuario1,usuario2,monto):
        """
        Permite transferir dinero de una cuenta a otra.
        Actualiza los saldos de los usuarios y los totales del banco y cajero.

        Args:
            usuario1: El objeto del usuario que realiza la transferencia.
            usuario2: El objeto del usuario que recibe la transferencia.
            monto: La cantidad de dinero a transferir.

        Returns:
            bool: True si la operación se realizó con éxito.
        """
        if usuario1.saldo >= monto:
            usuario1.saldo -= monto
            usuario2.saldo += monto
            self.dinerototal -= monto
            self.dinerocajero -= monto
            return True
        else:
            return False
    
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
        self.dinerototal -= usuario.saldo
        self.dinerocajero -= usuario.saldo
        return True

    def borrarcajero(self,cajero):
        """
        Permite eliminar un cajero del banco.
        Actualiza los totales del banco y cajero.

        Args:
            cajero: El objeto del cajero que se eliminará.

        Returns:
            bool: True si la operación se realizó con éxito.
        """
        self.cajerolist.remove(cajero)
        self.dinerocajero = self.dinerototal/len(self.cajerolist)
        return True
    