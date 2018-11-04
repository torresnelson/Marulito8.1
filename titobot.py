from pybot.usb4butia import USB4Butia
from calibracion import leerTatami, sensorGrisDer, sensorGrisIzq, sensorDistDel, sensorDistDer, velMotorIzq, velMotorDer
import time
import tabview as t

robot = USB4Butia()
sample = 1

prom = []

f = open('config', 'r') 
for i in range(4):
	prom.append(int(f.readline()))
f.close()

def router(port):
	if leerTatami(robot, port,sample) > prom[port-1]:
		return 1
	else: 
		return 0

def distancia(port):
	if robot.getDistance(port) < prom[2]:
		return 1
	else:
		return 0

raw_input('Coloque el dispositivo en la pista y presione enter para comenzar.')

routeIzq = router(sensorGrisIzq)
routeDer = router(sensorGrisDer)
distDel = distancia(sensorDistDel)
while (distDel == 0):
	distDel = distancia(sensorDistDel)
	routeIzq = router(sensorGrisIzq)
	routeDer = router(sensorGrisDer)
	robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
	print(str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(distDel))

distDer = distancia(sensorDistDer)
while (distDer == 0):
	distDer = distancia(sensorDistDer)
	routeIzq = 1
	routeDer = 0
	robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
	tabla = [['routeIzq','routeDer','distDel','distDer'], [routeIzq,routeDer,distDel,distDer]]
	t.view(tabla)

distDer = distancia(sensorGrisDer)

tabla = [['routeIzq','routeDer','distDel','distDer'], [routeIzq,routeDer,distDel,distDer]]
t.view(tabla)

while ((router(sensorGrisIzq) == 0) and (router(sensorGrisIzq) == 0)):
	distDer = distancia(sensorDistDer)
	if (distDer == 1):
		routeIzq = 0
		routeDer = 0
		robot.set2MotorSpeed(routeIzq, velMotorIzq, routeDer, velMotorDer)
	else:
		routeIzq = 0
		routeDer = 1
		robot.set2MotorSpeed(routeIzq, velMotorIzq, routeDer, velMotorDer)
	tabla = [['routeIzq','routeDer','distDel','distDer'], [routeIzq,routeDer,distDel,distDer]]
	t.view(tabla)
