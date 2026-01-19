from controller import Robot, Motor
import math

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# 1. OBTENER EL MOTOR
# En tu archivo .wbt le pusiste "aspa_motor_ct15"
motor = robot.getDevice("aspa_motor_ct15")

# 2. CONFIGURAR
target_pos = math.radians(51.43)

if motor:
    motor.setVelocity(2.0)
    motor.setPosition(target_pos)
    print("Servo CT15 activado.")
else:
    print("ERROR: No se encuentra 'aspa_motor_ct15'")

while robot.step(timestep) != -1:
    pass