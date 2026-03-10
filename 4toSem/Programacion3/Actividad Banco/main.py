"""
Aqui se Hace la ejecuscion de  todos los procesos

1. importar librerias
2. instanciar al banco
3. Instanciar objetos hilos - Cajeros y Clientes
4. Iniciar los ilos para que procesen las unciones correspondientes (.satart())
5. Hacer los joins()
6. Cerrar el banco
"""

### 1. Librerias y programas ##############

import os
import time
from Banco import Banco  # Del archivo Banco importa la clase Banco
from Clientes import Usuario
from Cajero import Cajero

############################################

os.system('clear')

## Variables 
nombre_banco = "Baniorte"
saldo_boveda = 1000000
num_clientes = 8
num_cajeros = 3
timeout = 20

#instanciar al banco
banco = Banco(nombre_banco, saldo_boveda,num_clientes,num_cajeros)

#creacion de hilos clientes y cajeros
cajeros = []
for i in range(num_cajeros):
    b = Cajero(i, banco)
    cajeros.append(b)

clientes = []
for i in range(num_clientes):
    c = Usuario(i, banco)
    clientes.append(c)

#Hacemos Joins a los hilos
for cliente in clientes:
    cliente.join(timeout=timeout)

banco.banco_abierto = False

# Notificamos a los cajeros que el banco cerro para que salgan del wait()
with banco.timbre:
    banco.timbre.notify_all()

for cajero in cajeros:
    cajero.join(timeout=timeout)

print("Banco cerrado")