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
from Banco import Banco #Del archivo Banco importa la clase Banco
from Clientes import usuario
from Cajero import cajero

############################################

os.system('clear')

## Variables 
nombre_banco = "Baniorte"
saldo_boveda = 1000000
num_clientes = 8
num_cajeros = 3

banco = Banco(nombre_banco, saldo_boveda)

banco.accion_cliente()