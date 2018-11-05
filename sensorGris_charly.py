from pybot.usb4butia import USB4Butia
from calibracion import leerTatami, sensorGrisDer, sensorGrisIzq

robot = USB4Butia()

while True:
    routeIzq = robot.getGray(sensorGrisIzq, 1)
    routeDer = robot.getGray(sensorGrisDer, 1)
    print(' Izquierdo: '+str(routeIzq)+' Derecho '+str(routeDer))
