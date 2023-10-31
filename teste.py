import threading
import time

# Função que gera uma interrupção após um determinado tempo
def timeout():
    print("Deu timeout")
    timer = threading.Timer(timeout_seconds, timeout)
    timer.start()

# Definindo o tempo limite para 5 segundos
timeout_seconds = 2

# Iniciando o temporizador
timer = threading.Timer(timeout_seconds, timeout)
timer.start()
i = 0
while True:
    print(i)
    i += 1
    time.sleep(5)
        
