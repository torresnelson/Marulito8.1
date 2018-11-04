from pybot.usb4butia import USB4Butia
from calibracion import leerTatami
import time


velMotorIzq = 150 + 100	
velMotorDer = 190 + 100

brd='1'
sleepTime = 1


robot = USB4Butia()

robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,board=brd)
time.sleep(sleepTime)

robot.set2MotorSpeed(1 , velMotorIzq, 1, velMotorDer, board=brd)
time.sleep(sleepTime)

robot.set2MotorSpeed(0, 0, 0, 0, board=brd)

