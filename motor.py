from pybot.usb4butia import USB4Butia
from calibracion import leerTatami, sensorGrisDer, sensorGrisIzq
from time import sleep

robot = USB4Butia()
robot.getModulesList()
sample = 1

prom = []

f = open('config', 'r') 
for i in range(6):
	prom.append(int(f.readline()))
f.close()

GRIS_DERECHA = prom[1];
GRIS_IZQUIERDA = prom[2];

PUERTO_DIST_CENTRAL = 3
PUERTO_DIST_LATERAL = 4

distObstaculoCentral = 47000
distObstaculoLateral = 48000
offset = 0  
velMotorSeguidor = 180
velocidadPala = 700

def router(port):
	if leerTatami(robot, port,sample) > prom[port]:
		return 1
	else: 
		return 0

def distanciaCentral():
	if robot.getDistance(PUERTO_DIST_CENTRAL) < distObstaculoCentral:
		return 1
	else:
		return 0

def distanciaLateral():
	if robot.getDistance(PUERTO_DIST_LATERAL) < distObstaculoLateral:
		return 1
	else:
		return 0

def adelante():
	robot.set2MotorSpeed(0 , velMotorSeguidor, 0, velMotorSeguidor,1)

def reversa():
	robot.set2MotorSpeed(1 , velMotorSeguidor, 1, velMotorSeguidor,1)

def giro_izquierda():
	robot.set2MotorSpeed(1 , velMotorSeguidor, 0, velMotorSeguidor,1)

def giro_derecha():
	robot.set2MotorSpeed(0 , velMotorSeguidor, 1, velMotorSeguidor,1)

def parar():
	robot.set2MotorSpeed(0, 0, 0, 0, 1)

def maruli_sleep(time):
	sleep((180 * time) / velMotorSeguidor)

def seguir_linea():
	robot.set2MotorSpeed(router(sensorGrisIzq) , velMotorSeguidor, router(sensorGrisDer), velMotorSeguidor)

def bajar_pala():
	robot.set2MotorSpeed(0,velocidadPala,0,velocidadPala,0)
	sleep(0.45)
	robot.set2MotorSpeed(0,0,0,0,0)

def subir_pala():
	robot.set2MotorSpeed(1,velocidadPala,1,velocidadPala,0)
	sleep(0.45)
	robot.set2MotorSpeed(0,0,0,0,0)

raw_input('Coloque el dispositivo en la pista y presione enter para comenzar.')


while True:
	while not(distanciaCentral()) and not(distanciaLateral()):
		seguir_linea()

	parar()
	sleep(1)

	if distanciaCentral():
		reversa()
		maruli_sleep(0.4)

		giro_izquierda()
		maruli_sleep(2)

		adelante()
		print('HARDCORE')
		maruli_sleep(1.5)

		while (not(router(sensorGrisIzq)) and not(router(sensorGrisDer))):
			flanco = distanciaLateral()
			if (flanco):
				adelante()
				maruli_sleep(0.1)
			else:
				giro_derecha()
				maruli_sleep(0.3)	

		adelante()
		while not(router(sensorGrisIzq)):
			pass

	if distanciaLateral():
		giro_derecha()
		while not distanciaCentral():
			pass

		parar()
		bajar_pala()
		sleep(1)
		subir_pala()
		sleep(120)
