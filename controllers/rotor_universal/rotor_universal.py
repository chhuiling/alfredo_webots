from controller import Robot, Motor
import math

robot = Robot()
timestep = int(robot.getBasicTimeStep())
nombre_robot = robot.getName() # <--- Aquí está la magia: "¿Quién soy?"

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

# --- VARIABLES DE MOVIMIENTO ---
target_rads = math.radians(51.43)
posicion_actual = 0 

# --- BUCLE PRINCIPAL ---
while robot.step(timestep) != -1:
    if receiver and receiver.getQueueLength() > 0:
        mensaje = receiver.getString()
        receiver.nextPacket()
        
        # Solo me muevo si la orden es EXACTAMENTE para mí
        if mensaje == mi_clave:
            print(f"[{nombre_robot}] Orden recibida. Girando...")
            posicion_actual += target_rads
            if motor:
                motor.setVelocity(2.0)
                motor.setPosition(posicion_actual)