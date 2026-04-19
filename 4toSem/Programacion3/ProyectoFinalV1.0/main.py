import modelo
# import graficas

def prediccion(modelo):
    resutado = modelo.predict([100.0])
    print(f'la temperatura {100.0}°C es igual a {resutado}°F')

if __name__ == '__main__':
    modelo, historial = modelo.entrenar_modelo()
    # graficas.graificas(historial)
    prediccion(historial)