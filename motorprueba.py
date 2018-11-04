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
	if robot.getDistance(port) < (prom[port]-15000):
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
while not(frente): #frente == 0
	frenteOrto = distanciaCentral(sensorDistDel)
	frenteDiag = distanciaLateral(sensorDistDel)
	frente = (frenteOrto) and (frenteDiag)
	routeIzq = router(sensorGrisIzq)
	routeDer = router(sensorGrisDer)
	robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
	print('fase 1: '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))

robot.set2MotorSpeed(routeIzq , 0, routeDer, 0)
raw_input('fase 1 completada,para continuar presione Enter')


flancoOrto = distanciaCentral(sensorDistDer)
flancoDiag = distanciaLateral(sensorDistDer)
while not(flancoOrto): #flanco == 0
	flancoOrto = distanciaCentral(sensorDistDer)
	flancoDiag = distanciaLateral(sensorDistDer)
	routeIzq = 1
	routeDer = 0
	robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
	print('fase 2: '+str(routeIzq)+' Izq  Der '+str(routeDer)+' sensorDistDer '+str(flancoOrto))
	time.sleep(0.4)

robot.set2MotorSpeed(routeIzq , 0, routeDer, 0)
time.sleep(2.5)
raw_input('fase 2 completada,para continuar presione Enter')


flancoOrto = distanciaCentral(sensorDistDer)
flancoDiag = distanciaLateral(sensorDistDer)
routeIzq = router(sensorGrisIzq)
routeDer = router(sensorGrisDer)
while (not(router(sensorGrisIzq)) and not(router(sensorGrisIzq))):
	
	flancoOrto = distanciaCentral(sensorDistDer)
	flancoDiag = distanciaLateral(sensorDistDer)
	if (flancoOrto):
		robot.set2MotorSpeed(0, velMotorIzq, 0, velMotorDer)
		time.sleep(0.1)
	else:
		robot.set2MotorSpeed(0, velMotorIzq, 1, velMotorDer)
		time.sleep(0.6)	
	print('fase 3: '+str(routeIzq)+' Izq  Der '+str(routeDer)+' sensorDistDer '+str(flanco))


robot.set2MotorSpeed(1, velMotorIzq, 0, velMotorDer+30)
print('fase 4: de vuelta a la linea')
time.sleep(1)	


#Reconocimiento de objeto fuera de la linea a la derecha
routeIzq = router(sensorGrisIzq)
routeDer = router(sensorGrisDer)
flancoOrto = distanciaCentral(sensorDistDer)
flancoDiag = distanciaLateral(sensorDistDer)
while not(flancoOrto):
	flancoOrto = distanciaCentral(sensorDistDer)
	routeIzq = router(sensorGrisIzq)
	routeDer = router(sensorGrisDer)
	robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
	print('fase 5: '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))

#Giro hacia la derecha, objeto fuera de la linea

frenteOrto = distanciaCentral(sensorDistDel)
frenteDiag = distanciaLateral(sensorDistDel) 
while not(frente): #frente == 0
	frenteOrto = distanciaCentral(sensorDistDel)
	routeIzq = 0
	routeDer = 1
	robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
	time.sleep(1)
	print('fase 6: '+str(routeIzq)+' Izq  Der '+str(routeDer)+' sensorDistDer '+str(flanco))