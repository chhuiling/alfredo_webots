from controller import Robot, Motor
import math

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# 1. Configurar Motor
motor = robot.getDevice("aspa_motor_ct12")
motor.setVelocity(2.0)
motor.setPosition(float('inf')) # Modo espera
motor.setVelocity(0) 

# 2. Configurar Receptor
receiver = robot.getDevice("receiver")
# Verificamos que exista para evitar el error rojo
if receiver is None:
    print("ERROR CRÍTICO: No encuentro el nodo Receiver. Revisa el árbol de nodos.")
else:
    receiver.enable(timestep)

MI_CLAVE = "MOVER_12" 
posicion_actual = 0 
target_rads = math.radians(51.43)

print(f"--- ROTOR 12: Escuchando en el canal... ---")

while robot.step(timestep) != -1:
    # Solo procesamos si el receptor existe y tiene mensajes
    if receiver and receiver.getQueueLength() > 0:
        
        # Leemos el mensaje (Webots nuevo usa getString)
        mensaje = receiver.getString()
        receiver.nextPacket() # Limpiamos el buzón
        
        if mensaje == MI_CLAVE:
            print(f"<< ROTOR 12: ¡Mensaje recibido! Girando...")
            posicion_actual += target_rads
            motor.setVelocity(2.0)
            motor.setPosition(posicion_actual)