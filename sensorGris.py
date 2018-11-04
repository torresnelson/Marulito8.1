from pybot.usb4butia import USB4Butia
from calibracion import leerTatami, sensorGrisDer, sensorGrisIzq

robot = USB4Butia()

while True:
	routeIzq = robot.getGray(sensorGrisIzq)
	routeDer = robot.getGray(sensorGrisDer)
	print(' Derecho '+str(routeIzq)+' Derecho '+str(routeDer))
