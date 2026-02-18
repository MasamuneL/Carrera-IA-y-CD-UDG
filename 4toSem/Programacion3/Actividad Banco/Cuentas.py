"""
Este Programa define la Clase Cuenta.

Atributos:
1. id_cuenta
2. CLABE
3. Saldo
4. Tipo de Cuenta
5. Estatus Buro
6. Id_usuario
7. Tokken

Metodos:
1. Retiro
2. Deposito
"""

class cuenta:
    def __init__(self,id,clabe,saldo,tipo,statusburo,user):
        self.Id = id
        self.clabe = clabe
        self.saldo = saldo
        self.tipo = tipo
        self.statusburo = statusburo
        self.user = user
        self.token = None

