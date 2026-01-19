from controller import Robot, Motor
import math

# Inicializar robot
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# 1. OBTENER EL MOTOR
# En tu archivo .wbt le pusiste el nombre "aspa_motor_ct12"
motor = robot.getDevice("aspa_motor_ct12")

# 2. CONFIGURAR EL MOVIMIENTO (51.43 grados)
target_pos = math.radians(51.43)

if motor:
    motor.setVelocity(2.0)          # Velocidad
    motor.setPosition(target_pos)   # Mover a la posición y frenar
    print("Servo CT12 activado: Moviendo a 51.43 grados.")
else:
    print("ERROR: No se encuentra 'aspa_motor_ct12'")

# 3. BUCLE DE SIMULACIÓN
while robot.step(timestep) != -1:
    pass