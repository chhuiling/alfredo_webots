from controller import Supervisor
import os
import winsound  # Usamos el audio de Windows directamente

# --- CONFIGURACIÓN ---
TIME_STEP = 32
TIEMPO_ALARMA = 5.0
TIEMPO_REGEN = 5.0

# --- RUTA DE AUDIO ---
# Calcula la ruta absoluta al archivo .wav automáticamente
directorio_actual = os.path.dirname(os.path.abspath(__file__))
RUTA_SONIDO = os.path.join(directorio_actual, "yo-phone-lining.wav")

# --- INICIALIZACIÓN ---
robot = Supervisor()

# 1. Obtener la Pastilla
pastilla_node = robot.getFromDef('PILL')
trans_field = None
posicion_inicial = None

if pastilla_node:
    trans_field = pastilla_node.getField('translation')
    posicion_inicial = trans_field.getSFVec3f()
else:
    print("ERROR: No encuentro 'DEF PILL'")

# 2. Obtener el Sensor (YA NO BUSCAMOS EL ALTAVOZ)
sensor_plato = robot.getDevice("sensor_plato")

if sensor_plato:
    sensor_plato.enable(TIME_STEP)
else:
    print("ERROR: No encuentro 'sensor_plato'")

# --- VARIABLES ---
ha_llegado_al_plato = False
timer_en_plato = 0.0
timer_fuera_plato = 0.0
alarma_activa = False

print("--- Supervisor (Modo Winsound) Iniciado ---")

while robot.step(TIME_STEP) != -1:
    if not pastilla_node or not sensor_plato: continue

    # Detectar contacto
    contacto = sensor_plato.getValue() > 0.0

    # =========================================================
    # CASO A: ALARMA (Pastilla olvidada en el plato)
    # =========================================================
    if contacto:
        ha_llegado_al_plato = True
        timer_fuera_plato = 0.0
        timer_en_plato += (TIME_STEP / 1000.0)

        # Si supera 5 segundos -> SONAR ALARMA DE WINDOWS
        if timer_en_plato > TIEMPO_ALARMA:
            if not alarma_activa:
                print("!!! ALARMA: Retire la pastilla !!!")
                alarma_activa = True
                
                # REPRODUCIR: 
                # SND_FILENAME: Es un archivo
                # SND_ASYNC: No congela la simulación
                # SND_LOOP: Repite hasta que le digamos que pare
                winsound.PlaySound(RUTA_SONIDO, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

    # =========================================================
    # CASO B: SILENCIAR Y REGENERAR
    # =========================================================
    else:
        timer_en_plato = 0.0
        
        # Si estaba sonando, mandamos la orden de PARAR (SND_PURGE)
        if alarma_activa:
            print(":) Pastilla retirada. Silenciando.")
            alarma_activa = False
            winsound.PlaySound(None, winsound.SND_PURGE)

        # Lógica de regeneración
        if ha_llegado_al_plato:
            timer_fuera_plato += (TIME_STEP / 1000.0)
            
            if timer_fuera_plato > TIEMPO_REGEN:
                print(">>> Ciclo completado. Regenerando pastilla...")
                pastilla_node.resetPhysics()
                
                if trans_field and posicion_inicial:
                    trans_field.setSFVec3f(posicion_inicial)
                
                # Resetear variables
                ha_llegado_al_plato = False
                timer_fuera_plato = 0.0
                timer_en_plato = 0.0
