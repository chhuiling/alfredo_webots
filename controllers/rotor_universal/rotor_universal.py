from controller import Robot, Motor, Speaker
import math

robot = Robot()
timestep = int(robot.getBasicTimeStep())
nombre_robot = robot.getName() # <--- Aquí está la magia: "¿Quién soy?"

# --- ZONA DE DIAGNÓSTICO ---
# print(f"====== DIAGNÓSTICO PARA {nombre_robot} ======")
# num_devices = robot.getNumberOfDevices()
# print(f"El robot tiene {num_devices} dispositivos conectados:")

# for i in range(num_devices):
    # dispositivo = robot.getDeviceByIndex(i)
    #Imprimimos el nombre REAL que ve el código
    # print(f" -> Dispositivo {i}: '{dispositivo.getName()}'") 
# print("============================================")

# --- CONFIGURACIÓN AUTOMÁTICA SEGÚN EL NOMBRE ---
motor_name = ""
mi_clave = ""

# Si soy el robot 12...
if "12" in nombre_robot:
    motor_name = "aspa_motor_ct12"
    mi_clave = "MOVER_12"

# Si soy el robot 15...
elif "15" in nombre_robot:
    motor_name = "aspa_motor_ct15"
    mi_clave = "MOVER_15"

# Si soy el robot 18...
elif "18" in nombre_robot:
    motor_name = "aspa_motor_ct18"
    mi_clave = "MOVER_18"

else:
    print(f"ERROR: No reconozco este robot: {nombre_robot}")

print(f"--- AUTO-CONFIGURACIÓN: Soy {nombre_robot}, controlo {motor_name} y espero {mi_clave} ---")

# --- INICIALIZACIÓN DE DISPOSITIVOS ---
motor = robot.getDevice(motor_name)
if motor:
    motor.setVelocity(2.0)
    motor.setPosition(float('inf'))
    motor.setVelocity(0)
else:
    print(f"ERROR CRÍTICO: No encuentro el motor {motor_name}")

receiver = robot.getDevice("receiver")
if receiver:
    receiver.enable(timestep)
    
# 1. INICIALIZAR EL ALTAVOZ
speaker = robot.getDevice("altavoz")
# No necesita 'enable', está siempre listo

if speaker:
    print(f"[{nombre_robot}] ¡ÉXITO! Altavoz encontrado.")
else:
    print(f"[{nombre_robot}] ERROR: Sigo sin encontrar un dispositivo llamado 'altavoz'. Revisa el nombre en el árbol.")

# --- VARIABLES DE MOVIMIENTO ---
target_rads = math.radians(51.43)
posicion_actual = 0
archivo_sonido = "./sounds/motor.wav" # La ruta relativa al controlador

# --- BUCLE PRINCIPAL ---
while robot.step(timestep) != -1:
    if receiver and receiver.getQueueLength() > 0:
        mensaje = receiver.getString()
        receiver.nextPacket()
        
        # Solo me muevo si la orden es EXACTAMENTE para mí
        if mensaje == mi_clave:
            print(f"[{nombre_robot}] Orden recibida. Girando...")
            
            # --- ZONA DE SONIDO ---
            if speaker:
                # IMPORTANTE: Los dos primeros argumentos son EL OBJETO speaker, no el volumen.
                # El volumen es el cuarto número (1.0)
                try:
                    speaker.playSound(speaker, speaker, archivo_sonido, 1.0, 1.0, 0.0, False)
                except Exception as e:
                    print(f"Error reproduciendo audio: {e}")
            # ----------------------    
            
            posicion_actual += target_rads
            if motor:
                motor.setVelocity(2.0)
                motor.setPosition(posicion_actual)