from pybot.usb4butia import USB4Butia
from calibracion import  boton

robot = USB4Butia()

while True:
	boton1 = robot.getButton(boton)
	print(str(boton1)+' <--- Boton1 ')