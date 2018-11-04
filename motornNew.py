from pybot.usb4butia import USB4Butia
from calibracion import leerTatami, sensorGrisDer, sensorGrisIzq, sensorDistDel, sensorDistDer, velMotorIzq, velMotorDer
import time

robot = USB4Butia()
sample = 1

prom = []

f = open('config', 'r') 
for i in range(6):
	prom.append(int(f.readline()))
f.close()

def router(port):
	if leerTatami(robot, port,sample) > prom[port]:
		return 1
	else: 
		return 0

def distanciaCentral(port):
	if robot.getDistance(port) < prom[port]:
		return 1
	else:
		return 0

def distanciaLateral(port):
	if robot.getDistance(port) < (prom[port]-10000):
		return 1
	else:
		return 0

raw_input('Coloque el dispositivo en la pista y presione enter para comenzar.')

frenteOrto = distanciaCentral(sensorDistDel)
frenteDiag = distanciaLateral(sensorDistDel)
flancoOrto = distanciaCentral(sensorDistDer)
flancoDiag = distanciaLateral(sensorDistDer)
frente = (frenteOrto) and (frenteDiag)
flanco = (flancoOrto) and (flancoDiag)
while not(frente) and not(flanco): #frente == 0
	frenteOrto = distanciaCentral(sensorDistDel)
	frenteDiag = distanciaLateral(sensorDistDel)
	flancoOrto = distanciaCentral(sensorDistDer)
	flancoDiag = distanciaLateral(sensorDistDer)
	frente = (frenteOrto) and (frenteDiag)
	flanco = (flancoOrto) and (flancoDiag)
	routeIzq = router(sensorGrisIzq)
	routeDer = router(sensorGrisDer)
	negro = (routeIzq) and (routeDer)
	if negro:
		robot.set2MotorSpeed(0 , velMotorIzq, 1, velMotorDer)
		time.sleep(0.6)
#		robot.set2MotorSpeed(0 , 0, 0, 0)
#		raw_input('Negroooooooo!!!!')
		robot.set2MotorSpeed(1 , 200, 0, 200)
		time.sleep(2)
		print('fase 1 recalculando: '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))
	else:
		robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
		time.sleep(0.1)
		print('fase 1 nornal      : '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))


	if (flancoOrto): #flanco == 0
		flancoOrto = distanciaCentral(sensorDistDer)
		routeIzq = 1
		routeDer = 0
		robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
		time.sleep(0.7)
		print('fase 2: '+str(routeIzq)+' Izq  Der '+str(routeDer)+' sensorDistDer '+str(flancoOrto))
		if (flancoOrto):
			robot.set2MotorSpeed(0, velMotorIzq, 0, velMotorDer)
			time.sleep(0.1)
		else:
			robot.set2MotorSpeed(0, velMotorIzq, 1, velMotorDer)
			time.sleep(0.6)	
		print('fase 3: '+str(routeIzq)+' Izq  Der '+str(routeDer)+' sensorDistDer '+str(flanco))

		
