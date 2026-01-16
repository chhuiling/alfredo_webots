from controller import Robot, Motor

# Crear la instancia del robot
robot = Robot()

# Obtener el paso de tiempo básico de la simulación
timestep = int(robot.getBasicTimeStep())

# 1. INICIALIZAR EL MOTOR
# Usamos el nombre que le dimos en el archivo .wbt
aspa_motor = robot.getDevice("motor_aspa")

# CONFIGURACIÓN DEL MODO DE GIRO:

# OPCIÓN A: Giro Continuo (como un ventilador/molino)
# 'inf' significa que no tiene límite de posición, girará por siempre.
aspa_motor.setPosition(float('inf'))
aspa_motor.setVelocity(2.0) # Velocidad en radianes/segundo

# OPCIÓN B: Comportamiento de Servo (ir a un ángulo específico)
# Si prefieres que se mueva a 90 grados y pare, descomenta estas lineas:
# aspa_motor.setPosition(1.57) # 1.57 radianes es aprox 90 grados
# aspa_motor.setVelocity(1.0)

# Bucle principal de simulación
while robot.step(timestep) != -1:
    # Aquí puedes añadir lógica. 
    # Por ejemplo, si usas la Opción B, podrías hacer que oscile:
    
    tiempo_actual = robot.getTime()
    if int(tiempo_actual) % 2 == 0:
        aspa_motor.setPosition(1.57) # Posición 1
    else:
        aspa_motor.setPosition(0.0)  # Posición 0
    
    pass