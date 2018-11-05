from pybot.usb4butia import USB4Butia
from calibracion_charly import leer_tatami
from calibracion_charly import sensorGrisDer
from calibracion_charly import sensorGrisIzq
from time import sleep

from globals_charly import *


robot = USB4Butia()
robot.getModulesList()
sample = 1

prom = []


with open('config', 'r') as f:
    for i in range(7):
        prom.append(int(f.readline()))


print('PROM:', prom)

GRIS_DERECHA = prom[1]
GRIS_IZQUIERDA = prom[2]

PUERTO_DIST_CENTRAL = 3
PUERTO_DIST_LATERAL = 4

distObstaculoCentral = 47000
distObstaculoLateral = 48000
offset = 0  
velMotorSeguidor = 180
velocidadPala = 700


def get_avg_sensor_color(port):
    print('Debugging')
    print('Port:', port)
    print('PROM:', prom)
    color_prom_port = prom[port]
    color = leer_tatami(robot, port, sample)

    if color > color_prom_port:
        return 'black'
    else: 
        return 'white'


def distanciaCentral():
    if robot.getDistance(PUERTO_DIST_CENTRAL) < distObstaculoCentral:
        return 'black'
    else:
        return 'white'


def distanciaLateral():
    if robot.getDistance(PUERTO_DIST_LATERAL) < distObstaculoLateral:
        return 'black'
    else:
        return 'white'


def adelante():
    robot.set2MotorSpeed(0 , velMotorSeguidor, 0, velMotorSeguidor, board_seguidor)


def reversa():
    robot.set2MotorSpeed(1 , velMotorSeguidor, 1, velMotorSeguidor, board_seguidor)


def giro_izquierda():
    robot.set2MotorSpeed(1 , velMotorSeguidor, 0, velMotorSeguidor, board_seguidor)


def giro_derecha():
    robot.set2MotorSpeed(0 , velMotorSeguidor, 1, velMotorSeguidor, board_seguidor)


def parar():
    robot.set2MotorSpeed(0, 0, 0, 0, board_seguidor)


def maruli_sleep(time):
    sleep((180 * time) / velMotorSeguidor)


def seguir_linea():
    robot.set2MotorSpeed(get_avg_sensor_color(sensorGrisIzq),
        velMotorSeguidor,
        get_avg_sensor_color(sensorGrisDer),
        velMotorSeguidor,
        board_seguidor
        )


def bajar_pala():
    robot.set2MotorSpeed(0, velocidadPala, 0, velocidadPala, board_pala)
    sleep(0.45)
    robot.set2MotorSpeed(0,0,0,0,0)


def subir_pala():
    robot.set2MotorSpeed(1, velocidadPala, 1, velocidadPala, board_pala)
    sleep(0.45)
    robot.set2MotorSpeed(0, 0, 0, 0, board_pala)


raw_input('Coloque el dispositivo en la pista y presione enter para comenzar.')

while True:
    #print('Gris der:', GRIS_DERECHA)
    #print('Gris izq:', GRIS_IZQUIERDA)
    avg_izq = get_avg_sensor_color(2)
    avg_der = get_avg_sensor_color(1)

    print('Avg_izq', avg_izq)
    print('Avg_der', avg_der)

    if not (avg_izq == 'black') or not(avg_der == 'black'):
        print('This extrange condition is here now.')

        robot.set2MotorSpeed(
            0,
            velMotorSeguidor,
            0,
            velMotorSeguidor,
            board_seguidor
        )
    elif (robot.getGray(sensorGrisIzq, board_seguidor) > GRIS_IZQUIERDA) and (robot.getGray(sensorGrisDer, board_seguidor) < GRIS_DERECHA):
        giro_izquierda()
    elif (robot.getGray(sensorGrisDer, board_seguidor) > GRIS_DERECHA) and (robot.getGray(sensorGrisIzq, board_seguidor) < GRIS_IZQUIERDA):
        giro_derecha()
    else:
        parar()

"""
while True:
    while not(distanciaCentral()) and not(distanciaLateral()):
        seguir_linea()

    parar()
    sleep(1)

    if distanciaCentral():
        reversa()
        maruli_sleep(0.4)

        giro_izquierda()
        maruli_sleep(2)

        adelante()
        print('HARDCORE')
        maruli_sleep(1.5)

        while (not(get_avg_sensor_color(sensorGrisIzq)) and not(get_avg_sensor_color(sensorGrisDer))):
            flanco = distanciaLateral()
            if (flanco):
                adelante()
                maruli_sleep(0.1)
            else:
                giro_derecha()
                maruli_sleep(0.3)   

        adelante()
        while not(get_avg_sensor_color(sensorGrisIzq)):
            pass

    if distanciaLateral():
        giro_derecha()
        while not distanciaCentral():
            pass

        parar()
        bajar_pala()
        sleep(1)
        subir_pala()
        sleep(120)
"""
