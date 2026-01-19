from controller import Robot, Emitter

robot = Robot()
timestep = int(robot.getBasicTimeStep())
emitter = robot.getDevice("emitter")

tiempo_actual = 0
tiempo_entre_giros = 0.1 # Segundos de espera entre cada uno
proximo_disparo = tiempo_entre_giros

# Lista de órdenes en secuencia
secuencia = ["MOVER_12", "MOVER_15", "MOVER_18"]
indice_actual = 0 # Empezamos por el primero de la lista (el 0 es el 12)

print("--- SUPERVISOR: Iniciando secuencia en bucle 12 -> 15 -> 18 ---")

while robot.step(timestep) != -1:
    tiempo_actual += timestep / 1000.0
    
    if tiempo_actual >= proximo_disparo:
        # 1. Elegir la orden que toca
        orden = secuencia[indice_actual]
        
        # 2. Enviar la orden
        emitter.send(orden.encode('utf-8'))
        print(f">> SUPERVISOR: Turno del {orden} (Time: {tiempo_actual:.1f}s)")
        
        # 3. Preparar el siguiente turno
        # El operador % (módulo) hace que al llegar a 3 vuelva a 0 (0, 1, 2, 0, 1, 2...)
        indice_actual = (indice_actual + 1) % len(secuencia)
        
        # 4. Programar el siguiente tiempo
        proximo_disparo += tiempo_entre_giros
        
    if tiempo_entre_giros < 1:
        tiempo_entre_giros = 15
