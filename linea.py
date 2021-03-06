from pybot.usb4butia import USB4Butia
from calibracion import leerTatami, sensorGrisDer, sensorGrisIzq, sensorDistDel, sensorDistDer, velMotorDer, velMotorIzq
from time import sleep

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
	if robot.getDistance(port,1) < prom[port]:
		return 1
	else:
		return 0

def distanciaLateral(port):
	if robot.getDistance(port,1) < (prom[port]-10000):
		return 1
	else:
		return 0

raw_input('Coloque el dispositivo en la pista y presione enter para comenzar.')

while True:
	frenteOrto = distanciaCentral(sensorDistDel)
	frenteDiag = distanciaLateral(sensorDistDel)
	frente = (frenteOrto) and (frenteDiag)
	flanco = distanciaCentral(sensorDistDer)
	while not(frente) : #frente == 0
		frenteOrto = distanciaCentral(sensorDistDel)
		frenteDiag = distanciaLateral(sensorDistDel)
		routeIzq = router(sensorGrisIzq)
		routeDer = router(sensorGrisDer)
		frente = (frenteOrto) and (frenteDiag)
		robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer,1)
		if routeDer and routeIzq:
			robot.set2MotorSpeed(1 , velMotorIzq+30, 1, velMotorDer,1)
			sleep(0.5)
		print('fase 1 normal        : '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))

	robot.set2MotorSpeed(1 , velMotorIzq, 1, velMotorDer,1)
	sleep(0.5)
	print('reversa')

	robot.set2MotorSpeed(1 , velMotorIzq, 0, velMotorDer,1)
	sleep(2.5)
	print('giro')

	robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,1)
	sleep(1)
	print('hardcore parkour')
		
	while (not(router(sensorGrisIzq)) and not(router(sensorGrisDer))):
		flanco = distanciaCentral(sensorDistDer)
		if (flanco):
			robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,1)
			sleep(0.1)
		else:
			robot.set2MotorSpeed(0 , velMotorIzq+30, 1, velMotorDer,1)
			sleep(0.3)

	robot.set2MotorSpeed(1 , velMotorIzq+30, 0, velMotorDer,1)
	sleep(2.5)

	while not(flanco) : #frente == 0
		routeIzq = router(sensorGrisIzq)
		routeDer = router(sensorGrisDer)
		flanco = distanciaCentral(sensorDistDer)
		robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer,1)
		if routeDer and routeIzq:
			robot.set2MotorSpeed(1 , velMotorIzq+30, 1, velMotorDer,1)
			sleep(0.5)
		print('fase 2 normal        : '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))

	robot.set2MotorSpeed(1 , velMotorIzq, 1, velMotorDer, 1)
	sleep(0.5)
	print('reversa')

	robot.set2MotorSpeed(0 , velMotorIzq, 1, velMotorDer,1)
	sleep(2)
	print('giro')


	robot.set2MotorSpeed(0 , 180, 0, 0,0)
	sleep(0.6)
	print('pala')


	robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,1)
	sleep(2)
	print('avance')


	robot.set2MotorSpeed(1 , velMotorIzq, 0, velMotorDer, 1)
	sleep(4)
	print('360')

	while (not(router(sensorGrisIzq)) and not(router(sensorGrisDer))):
		routeIzq = router(sensorGrisIzq)
		routeDer = router(sensorGrisDer)
		robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,1)

	robot.set2MotorSpeed(0 , velMotorIzq, 1, velMotorDer+30,1)
	sleep(2)					

	while not(flanco) or not(frente) : #frente == 0
		routeIzq = router(sensorGrisIzq)
		routeDer = router(sensorGrisDer)
		flanco = distanciaCentral(sensorDistDer)
		frente = distanciaCentral(sensorDistDel)
		robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer,1)
		
		if routeDer and routeIzq:
			robot.set2MotorSpeed(0 , velMotorIzq ,0, velMotorDer,1)
			sleep(0.1)
			if routeDer and routeIzq:
				robot.set2MotorSpeed(0 , velMotorIzq ,0, velMotorDer,1)
				sleep(0.1)
		else:
			robot.set2MotorSpeed(1 , velMotorIzq ,1, velMotorDer,1)
			sleep(0.3)
		
		if (flanco):
			robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,1)
			sleep(2.5)	
		
		if (frente):
			robot.set2MotorSpeed(1 , velMotorIzq, 0, velMotorDer,1)
			sleep(2.5)
		
		if routeDer and routeIzq:
			robot.set2MotorSpeed(1 , velMotorIzq, 1, velMotorDer,1)
			sleep(2.5)
			
		print('fase final        : '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))