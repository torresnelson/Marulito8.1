from pybot.usb4butia import USB4Butia
from calibracion import leerTatami, sensorGrisDer, sensorGrisIzq, sensorDistDel, sensorDistDer, velMotorIzq, velMotorDer
import time

robot = USB4Butia()
pala = USB4Butia()
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


while True:
	frenteOrto = distanciaCentral(sensorDistDel)
	frenteDiag = distanciaLateral(sensorDistDel)
	flancoOrto = distanciaCentral(sensorDistDer)
	flancoDiag = distanciaLateral(sensorDistDer)
	frente = (frenteOrto) and (frenteDiag)
	flanco = (flancoOrto) and (flancoDiag)
	while not(frente): #frente == 0
		frenteOrto = distanciaCentral(sensorDistDel)
		frenteDiag = distanciaLateral(sensorDistDel)
		flancoOrto = distanciaCentral(sensorDistDer)
		flancoDiag = distanciaLateral(sensorDistDer)
		routeIzq = router(sensorGrisIzq)
		routeDer = router(sensorGrisDer)
		frente = (frenteOrto) and (frenteDiag)
		robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer)
		print('fase 1 normal        : '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))
		
	robot.set2MotorSpeed(1 , velMotorIzq, 1, velMotorDer,'0')
	time.sleep(0.4)
	print('fase 1 normal reverse: '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))


	robot.set2MotorSpeed(1 , velMotorIzq, 0, velMotorDer,'0')
	time.sleep(2)

	robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,'0')
	print('HARDCORE')
	time.sleep(1.5)

		
	#robot.set2MotorSpeed(routeIzq , 0, routeDer, 0)
	#raw_input('fase 2 completada,para continuar presione Enter')

	flancoOrto = distanciaCentral(sensorDistDer)
	routeIzq = router(sensorGrisIzq)
	routeDer = router(sensorGrisDer)
	blanco = (not(router(sensorGrisIzq)) and not(router(sensorGrisIzq)))
	while (blanco):
		blanco = (not(router(sensorGrisIzq)) and not(router(sensorGrisIzq)))
		flancoOrto = distanciaCentral(sensorDistDer)
		if (flancoOrto):
			robot.set2MotorSpeed(0, velMotorIzq, 0, velMotorDer,'0')
			time.sleep(0.1)
		else:
			robot.set2MotorSpeed(0, velMotorIzq, 1, velMotorDer,'0')
			time.sleep(0.3)	
		print('fase 3: '+str(routeIzq)+' Izq  Der '+str(routeDer)+' sensorDistDer '+str(flanco))

	routeIzq = router(sensorGrisIzq)
	routeDer = router(sensorGrisDer)
	blanco = (not(router(sensorGrisIzq)) and not(router(sensorGrisIzq)))
	if not(blanco):			

		robot.set2MotorSpeed(1, velMotorIzq+50, 0, velMotorDer,'0')
		print('fase 4: de vuelta a la linea')
		time.sleep(2)	

