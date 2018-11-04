from pybot.usb4butia import USB4Butia

#Blanco = 0
#Negro = 1
#Motor1 = izq
#Motor2 = der

sensorGrisDer = 1
sensorGrisIzq = 2


def leerTatami(bot, port, sample):
	acumLectura = 0
	for i in range(sample):
		acumLectura += bot.getGray(port)
	return acumLectura / sample

def obtenerCalibracion(bot, sample):

	promBlDer = 0
	promNeDer = 0
	promBlIzq = 0
	promNeIzq = 0

	
	raw_input('Coloque el dispositivo en una superficie blanca y presione enter paran continuar.')
	promBlDer = leerTatami(bot, sensorGrisDer, sample)
	promBlIzq = leerTatami(bot, sensorGrisIzq, sample)

	raw_input('Coloque el dispositivo en una superficie negra y presione enter paran continuar.')
	promNeDer = leerTatami(bot, sensorGrisDer, sample)
	promNeIzq = leerTatami(bot, sensorGrisIzq, sample)


	promTotalDer = (promBlDer + promNeDer) / 2
	promTotalIzq = (promBlIzq + promNeIzq) / 2

	return [promTotalDer,promTotalIzq]

if __name__ == "__main__":
	robot = USB4Butia()
	valores = obtenerCalibracion(robot, 1000)
	f = open('config','w')
	f.write(str(valores[0])+'\n')
	f.write(str(valores[1])+'\n')
	f.close()
	raw_input('Calibracion terminada')
