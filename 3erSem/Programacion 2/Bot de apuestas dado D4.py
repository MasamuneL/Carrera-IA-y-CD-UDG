# "bot" de apuestas dado D4
import os
import random
os.system('say "Lets Go gambling!"') 
fichas = 10
rondas = 5
d4 = 4
for ronda in range(rondas):
    if fichas <= 0:
        os.system(f'say "Te quedaste sin fichas"')
        break
    os.system(f'say "Tus fichas actuales son {fichas}"')
    apuesta = random.randint(1,fichas)
    os.system(f'say "Apuesto {apuesta} fichas al {d4}"')
    try:
        resultado = input("Ganaste o perdiste? (Escribe 'si' o 'no')")
        if resultado == "si":
            fichas = fichas + apuesta
            os.system(f'say "Genial ganaste {apuesta} fichas, en total tienes: {fichas} fichas"')
        else:
            fichas = fichas - apuesta
            os.system(f'say "Lastima perdiste {apuesta} fichas, en total tienes: {fichas} fichas"')
        os.system(f'Listo para la siguiente ronda?"')
    except ValueError:
            print("escribe si o no")
    
    try:
        sigronda = input("Listo para la siguiente ronda?")
        while sigronda != "si":
            os.system(f'say "Te espero"')
            sigronda = input("Listo para la siguiente ronda?")
        else:
            os.system(f'say "Perfecto, siguiente ronda!"')
    except ValueError:
        print("respuesta no valida")
os.system(f'say "Terminamos las {rondas} rondas, acabaste con un total de {fichas} fichas!"')
        
            