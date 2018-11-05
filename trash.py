'''
	while (not(router(sensorGrisIzq)) and not(router(sensorGrisDer))):
		flanco = distanciaCentral(sensorDistDer)
		if (flanco):
			robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,1)
			sleep(0.1)
		else:
			robot.set2MotorSpeed(0 , velMotorIzq+30, 1, velMotorDer,1)
			sleep(0.3)
		robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,1)

	robot.set2MotorSpeed(0 , velMotorIzq, 1, velMotorDer, 1)
	sleep(5)
	print('360')

	robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,1)
	sleep(2.5)
	print('giro')

	robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,1)
	sleep(2)
	print('hardcore parkour')
	
	
	robot.set2MotorSpeed(0 , 200, 0, 0,0)
	sleep(1)
	robot.set2MotorSpeed(0 , 0, 0, 0,0)
	
	while (not(router(sensorGrisIzq)) and not(router(sensorGrisDer))):
		routeIzq = router(sensorGrisIzq)
		routeDer = router(sensorGrisDer)
		robot.set2MotorSpeed(0 , velMotorIzq, 0, velMotorDer,1)


	robot.set2MotorSpeed(1 , velMotorIzq+30, 0, velMotorDer,1)
	sleep(2)					
'''