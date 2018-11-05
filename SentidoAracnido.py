from pybot.usb4butia import USB4Butia
from calibracion import  boton, sensorGrisDer, sensorGrisIzq, sensorDistDel, sensorDistDer, leerTatami

robot = USB4Butia()
sample = 1
prom = []

f = open('config', 'r') 
for i in range(3):
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

while True:
	routeIzq = router(sensorGrisIzq)
	routeDer = router(sensorGrisDer)
	distDel = distancia(sensorDistDel)
	distDer = distancia(sensorDistDer)
	boton1 = robot.getButton(boton)
	print(str(routeIzq)+' <--GrisIzq  GrisDer--> '+str(routeDer)+'	'+str(distDel)+' <---DistDel '+str(distDer)+' <--- DistDer '+str(boton1)+' <--- Boton1 ')

	
