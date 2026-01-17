from controller import Robot, Motor
import math

robot = Robot()
timestep = int(robot.getBasicTimeStep())

aspa_motor = robot.getDevice("aspa_motor_ct18")

# Convertir 51.43 grados a radianes
target_pos = math.radians(51.43)

aspa_motor.setVelocity(2.0)
aspa_motor.setPosition(target_pos)

while robot.step(timestep) != -1:
    pass