from pybot.usb4butia import USB4Butia
import time
from calibracion import leerTatami, sensorGrisDer, sensorGrisIzq, sensorDistDel, sensorDistDer, velMotorIzq, velMotorDer

robot = USB4Butia()
sample = 1

prom = []

f = open('config', 'r') 
for i in range(3):
	prom.append(int(f.readline()))
f.close()

def router(port):
	print
	if leerTatami(robot, port,sample) > prom[port-1]:
		return 1
	else: 
		return 0

def distancia(port):
	if robot.getDistance(port) > prom[2]:
		return 0
	else:
		return 1
raw_input('Coloque el dispositivo en la pista y presione enter para comenzar.')

routeIzq = router(sensorGrisIzq)
routeDer = router(sensorGrisDer)
frente = distancia(sensorDistDel)
while (True):
	
	routeIzq = router(sensorGrisIzq)


	routeDer = router(sensorGrisDer)

	if(routeIzq and routeDer):
		robot.set2MotorSpeed(not(routeIzq) , velMotorIzq, not(routeDer), velMotorDer)
		time.sleep(1)
		robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
		time.sleep(1)
		robot.set2MotorSpeed(not(routeIzq) , velMotorIzq, not(routeDer), velMotorDer)
		time.sleep(1)

	robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
	print(str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))

