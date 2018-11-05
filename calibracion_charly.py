from pybot.usb4butia import USB4Butia

from globals_charly import *

# Blanco = 0
# Negro = 1
# Motor1 = izq
# Motor2 = der


sensorGrisDer = 1
sensorGrisIzq = 2
sensorDistDel = 3
sensorDistDer = 4
boton = 5
distObstaculoFrente = 47000
distObstaculoDerecha = 48000
offset = 0
velMotorDer = 150 + offset 
velMotorIzq = 150


def leer_tatami(bot, port, sample):
    acum_lectura = 0

    for i in range(sample):
        acum_lectura += bot.getGray(
            port=port,
            board=board_seguidor
            )

    return acum_lectura / sample


def obtenerCalibracion(bot, sample):
    promBlDer = 0
    promNeDer = 0
    promBlIzq = 0
    promNeIzq = 0

    raw_input('Coloque el dispositivo en una superficie blanca y presione enter paran continuar.')
    promBlDer = leer_tatami(bot, sensorGrisDer, sample)
    promBlIzq = leer_tatami(bot, sensorGrisIzq, sample)

    raw_input('Coloque el dispositivo en una superficie negra y presione enter paran continuar.')
    promNeDer = leer_tatami(bot, sensorGrisDer, sample)
    promNeIzq = leer_tatami(bot, sensorGrisIzq, sample)


    promTotalDer = (promBlDer + promNeDer) / 2
    promTotalIzq = (promBlIzq + promNeIzq) / 2

    #return [offset, promTotalDer, promTotalIzq, distObstaculoFrente, distObstaculoDerecha, velMotorDer, velMotorIzq]
    return offset, promTotalDer, promTotalIzq, distObstaculoFrente, distObstaculoDerecha, velMotorDer, velMotorIzq


if __name__ == '__main__':
    robot = USB4Butia()
    # valores = obtenerCalibracion(robot, 1000)
    offset, promTotalDer, promTotalIzq, distObstaculoFrente, distObstaculoDerecha, velMotorDer, velMotorIzq = obtenerCalibracion(robot, 1000)

    with open('config', 'w') as f:
        f.write(str(offset) + '\n')
        f.write(str(promTotalDer) + '\n')
        f.write(str(promTotalIzq) + '\n')
        f.write(str(distObstaculoFrente) + '\n')
        f.write(str(distObstaculoDerecha) + '\n')
        f.write(str(velMotorDer) + '\n')
        f.write(str(velMotorIzq) + '\n')

    raw_input('Calibracion terminada')
