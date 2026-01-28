def suma(a,b):
    try:
        sum = a + b
        return sum
    except ValueError:
        return print("Valor no valido") 
    
def promedio(lista):
    prom = 0
    if len(lista) == 0:
        return 0
    else:
        for i in lista:
            prom = prom + i
        prom = prom/len(lista)
        return prom

def factorial(x):
    factx = x
    try:
        if x < 0:
            raise ValueError
        elif x == 0:
            return 1
        else:
            while x > 1:
                x = x-1
                factx = factx * x
            return factx
    except ValueError:
        raise ValueError
    
def primeraMayusc(palabra):
    try:
        palabra[0].upper()
    except ValueError:
        return print("La primera letra ya esta en mayuscula o el valor no es valido")
