import winsound
import os

# 1. Obtiene la carpeta donde vive ESTE archivo .py (no desde donde se ejecuta)
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# 2. Une esa carpeta con el nombre del archivo (Ruta Absoluta)
ruta_completa_audio = os.path.join(directorio_actual, "yo-phone-lining.wav")

print(f"Buscando audio en: {ruta_completa_audio}")

# 3. Reproducir usando la ruta a prueba de balas
try:
    winsound.PlaySound(ruta_completa_audio, winsound.SND_FILENAME)
except Exception as e:
    print("Error:", e)