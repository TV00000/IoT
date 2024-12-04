import time
from lib.buttonLED import buttonLED
from lib.ledstick import ledStick

class Gateway:
	def __init__(self):
		print("Initialisation de la passerelle")
		self.bLed1 = buttonLED.GroveButtonLed(6,5)
		self.bLed2 = buttonLED.GroveButtonLed(17,16)
		self.LEDStick = ledStick.GroveLedStick(12,10)	
		self.numberLedStickLED=-1

		
	def inputUpdate(self):
		print("Mise à jour des entrées")
		self.status_b1 = self.bLed1.getStatusButton()
		self.status_b2 = self.bLed2.getStatusButton()

	def inputProcessing(self):
		print("Traitement des entrées")
		if self.status_b1 == 0 :
			if self.numberLedStickLED < 10 :
				self.numberLedStickLED += 1
		else :
			self.numberLedStickLED = -1
	
	def graph(self):
		print("Graph d'état")

	def outputProcessing(self):
		print("Traitement des sorties")

	def outputUpdate(self):
		print("Traitement des sorties")
		self.bLed1.setStatusLed(not(self.status_b1))
		self.bLed2.setStatusLed(not(self.status_b2))
		if self.numberLedStickLED > -1 :
			self.LEDStick.LedRGB_ON(self.numberLedStickLED, 0, 0, 255)
		else : 
			self.LEDStick.LedRGB_AllOFF()
