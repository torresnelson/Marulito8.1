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
	if robot.getDistance(port) > (prom[port]-1000):
		return 1
	else:
		return 0

raw_input('Coloque el dispositivo en la pista y presione enter para comenzar.')

routeIzq = router(sensorGrisIzq)
routeDer = router(sensorGrisDer)
frenteOrto = distanciaCentral(sensorDistDel)
frenteDiag = distanciaLateral(sensorDistDel)
flancoOrto = distanciaCentral(sensorDistDer)
flancoDiag = distanciaLateral(sensorDistDer)
frente = (frenteOrto) and (frenteDiag)
flanco = (flancoOrto) and (flancoDiag)
while not(frente) or not(flanco): #frente == 0 
	frenteOrto = distanciaCentral(sensorDistDel)
	frenteDiag = distanciaLateral(sensorDistDel)
	flancoOrto = distanciaCentral(sensorDistDer)
	flancoDiag = distanciaLateral(sensorDistDer)
	frente = (frenteOrto) and (frenteDiag)
	flanco = (flancoOrto) and (flancoDiag)
	if not(frente) :
		routeIzq = router(sensorGrisIzq)
		routeDer = router(sensorGrisDer)
		frenteOrto = distanciaCentral(sensorDistDel)
		frenteDiag = distanciaLateral(sensorDistDel)
		frente = (frenteOrto) and (frenteDiag)
		robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
		time.sleep(0.1)
		print('Linea: Izq '+str(routeIzq)+' Der '+str(routeDer)+'  sensorDistDelantero '+str(frenteOrto))
	else:
		robot.set2MotorSpeed(1 , velMotorIzq, 0, velMotorDer)
		time.sleep(0.5)
		robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer)
		time.sleep(0.5)
		print('Obstaculo: Izq '+str(routeIzq)+' Der '+str(routeDer)+' sensorDistDererecho '+str(flancoOrto))
		while (not(router(sensorGrisIzq)) and not(router(sensorGrisIzq))):
			if (flanco):
				robot.set2MotorSpeed(0, velMotorIzq, 0, velMotorDer)
				time.sleep(0.3)
			else:
				robot.set2MotorSpeed(0, velMotorIzq, 1, velMotorDer)
				time.sleep(0.6)	
			print('Esquivando: Izq '+str(routeIzq)+' Der '+str(routeDer)+' sensorDistDerecho '+str(flancoOrto))
	
	if (flanco):
		robot.set2MotorSpeed(1 , velMotorIzq, 0, velMotorDer)
		time.sleep(0.5)
		robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer)
		time.sleep(0.5)
		while frente:
			robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer)
			
		print('Objeto a la derecha: Izq '+str(routeIzq)+' Der '+str(routeDer)+' sensorDistDererecho '+str(flancoOrto))




raw_input('Iniciar fase 2.')

