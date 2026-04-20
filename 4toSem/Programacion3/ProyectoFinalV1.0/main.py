import modelo
import os
from tensorflow import keras
# import graficas

RUTA_MODELO = "modelo_entrenado.keras"

def guardar_modelo(modelo_entrenado, ruta=RUTA_MODELO):
    modelo_entrenado.save(ruta)
    print(f'✅ Modelo guardado en: {os.path.abspath(ruta)}')

def cargar_modelo(ruta=RUTA_MODELO):
    if os.path.exists(ruta):
        modelo_cargado = modelo.load_model(ruta)
        print(f'✅ Modelo cargado desde: {os.path.abspath(ruta)}')
        return modelo_cargado
    else:
        print(f'❌ No se encontró el modelo en: {os.path.abspath(ruta)}')
        return None
    
def prediccion(modelo):
    resutado = modelo.predict([100.0])
    print(f'la temperatura {100.0}°C es igual a {resutado}°F')

if __name__ == '__main__':
    modelo_entrenado = cargar_modelo()

    if modelo_entrenado is None:
        print("No hay modelo entenado. Entrenando...")
        modelo_entrenado, historial = modelo.entrenar_modelo()
        guardar_modelo(modelo_entrenado)