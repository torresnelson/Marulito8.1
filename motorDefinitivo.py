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

def distanciaLateral(port):
	if robot.getDistance(port) < (prom[port]-10000):
		return 1
	else:
		return 0


#Blanco = 0
#Negro = 1
#Motor1 = izq
#Motor2 = der

raw_input('Coloque el dispositivo en la pista y presione enter para comenzar.')

frenteOrto = distanciaCentral(sensorDistDel)
frenteDiag = distanciaLateral(sensorDistDel)
flancoOrto = distanciaCentral(sensorDistDer)
flancoDiag = distanciaLateral(sensorDistDer)
frente = (frenteOrto) and (frenteDiag)
flanco = (flancoOrto) and (flancoDiag)
routeIzq = router(sensorGrisIzq)
routeDer = router(sensorGrisDer)

while (True): 
	frenteOrto = distanciaCentral(sensorDistDel)
	frenteDiag = distanciaLateral(sensorDistDel)
	flancoOrto = distanciaCentral(sensorDistDer)
	flancoDiag = distanciaLateral(sensorDistDer)
	routeIzq = router(sensorGrisIzq)
	routeDer = router(sensorGrisDer)
	while not(frente): #frente == 0
		frenteOrto = distanciaCentral(sensorDistDel)
		frenteDiag = distanciaLateral(sensorDistDel)
		flancoOrto = distanciaCentral(sensorDistDer)
		flancoDiag = distanciaLateral(sensorDistDer)
		routeIzq = router(sensorGrisIzq)
		routeDer = router(sensorGrisDer)
		frente = (frenteOrto) and (frenteDiag)
		robot.set2MotorSpeed(routeIzq , velMotorIzq, routeDer, velMotorDer,'0')
		print('fase 1: sobre la linea: '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))
		
		dosnegros = routeIzq and routeDer
		
		if (dosnegros):
			robot.set2MotorSpeed( 0, velMotorIzq, 0, velMotorDer,'0')
			time.sleep(0.1)
			print('fase 1: REVERSA '+str(routeIzq)+' Izq   Der '+str(routeDer)+'  sensorDistDel '+str(frente))
			if routeDer:
				robot.set2MotorSpeed(0 , velMotorIzq, 1, velMotorDer,'0')
				time.sleep(0.1)
				robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,'0')
				time.sleep(0.1)

			if routeIzq:
				robot.set2MotorSpeed(1 , velMotorIzq, 0, velMotorDer,'0')
				time.sleep(0.1)
				robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,'0')
				time.sleep(0.1)
								
	robot.set2MotorSpeed(1 , velMotorIzq, 1, velMotorDer,'0')
	time.sleep(0.1)
	print('fase 0.1: reverse')

	robot.set2MotorSpeed(1 , velMotorIzq, 0, velMotorDer,'0')
	time.sleep(1.8)
	print('fase 2: Giro a la derecha')
	
	robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,'0')
	time.sleep(1.8)
	print('fase 2: Avance HARDCORE')
	
	flancoOrto = distanciaCentral(sensorDistDer)
	routeIzq = router(sensorGrisIzq)
	routeDer = router(sensorGrisDer)
	negro = (router(sensorGrisIzq) and router(sensorGrisIzq))
	while not(negro):
		negro = (router(sensorGrisIzq) and router(sensorGrisIzq))
		routeIzq = router(sensorGrisIzq)
		routeDer = router(sensorGrisDer)
		flancoOrto = distanciaCentral(sensorDistDer)
		if (flancoOrto):
			robot.set2MotorSpeed(0, velMotorIzq, 0, velMotorDer)
			time.sleep(0.1)
		else:
			robot.set2MotorSpeed(0, velMotorIzq+30, 1, velMotorDer)
			time.sleep(0.1)	
		print('fase 2: ESQUIVANDO '+str(routeIzq)+' Izq  Der '+str(routeDer)+' sensorDistDer '+str(flanco))

	routeIzq = router(sensorGrisIzq)
	routeDer = router(sensorGrisDer)
	negro = (router(sensorGrisIzq) and router(sensorGrisIzq))
	if negro:
		robot.set2MotorSpeed(1, velMotorIzq, 0, velMotorDer)
		print('fase 2: VUELVE A LA LINEA')
		time.sleep(0.6)
		robot.set2MotorSpeed(0, 0, 0, 0)
		raw_input('listo')