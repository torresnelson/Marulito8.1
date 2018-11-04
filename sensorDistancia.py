from pybot.usb4butia import USB4Butia
from calibracion import  sensorDistDer, sensorDistDel

robot = USB4Butia()

prom = []

f = open('config', 'r') 
for i in range(3):
	prom.append(int(f.readline()))
f.close()

def distancia(port):
	if robot.getDistance(port) > prom[2]:
		return 0
	else:
		return 1

while True:
	distDel = robot.getDistance(sensorDistDel)
	distDer = robot.getDistance(sensorDistDer)
	print(str(distDel)+' <--- DistDel '+str(distDer)+' <--- DistDer ')
