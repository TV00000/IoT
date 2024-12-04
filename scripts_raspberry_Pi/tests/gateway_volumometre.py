import time
from lib.ledstick.ledStick import GroveLedStick 
from lib.sensorSound.sensorSound import GroveSoundSensor


class Gateway:
	def __init__(self):
		print("Initialisation de la passerelle")
		self.LEDStick = GroveLedStick(12,10)	
		self.numberLedStickLED=-1
		self.soundSensor = GroveSoundSensor(0)
		self.noise = 0 

		
	def inputUpdate(self):
		print("Mise à jour des entrées")
		self.noise = self.soundSensor.getRawSensorValue()
		

	def inputProcessing(self):
		print("Traitement des entrées")
		# On remet le nombre de LED allumee a sa valeur initiale
		# Cela permet d'eviter de rester avec toutes les LED allumees
		# quand le max est atteint
		self.numLedStickLED = -1
		# Adaptation du nombre de LED allumee en fonction 
		# du volume sonore
		self.numLedStickLED = self.numLedStickLED + self.noise //50
		print(self.numLedStickLED)

	def graph(self):
		print("Graph d'état")

	def outputProcessing(self):
		print("Traitement des sorties")

	def outputUpdate(self):
		print("Traitement des sorties")
		if self.numLedStickLED > -1 :
			self.LEDStick.LedRGB_N_ON(self.numLedStickLED, 0, 0, 255)
		else : 
			self.LEDStick.LedRGB_AllOFF()
