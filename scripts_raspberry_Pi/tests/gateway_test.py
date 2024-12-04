
import time
import datetime
from lib.ledstick.ledStick import GroveLedStick 
from lib.sensorSound.sensorSound import GroveSoundSensor
from lib.buttonLED.buttonLED import GroveButtonLed
from lib.sensorDHT.sensorDHT import GroveDHTSensor
from lib.sensorPIR.sensorPIR import GrovePirMotionSensor
from lib.sensorAirquality.sensorAirquality import GroveAirQualitySensor
from lib.buzzer.buzzer import GroveBuzzer

class Gateway:
	def __init__(self):
		print("Initialisation de la passerelle")
		# flux de données
		self.data_JSON = []
		self.dico_data_JSON = {"temperature" : 0,"humidity" : 0, "noise" : 0, "isPeopleDetected" : 0, "TVoC" : 0, "CO2eq": 0}
		self.liste_input_CSV = []
		self.liste_entete =["time", "temperature", "humidity", "noise", "isPeopleDetected", "TVoC", "CO2eq"]
		# initialisation du fichier csv 
		with open("all_data.csv", "w") as f:
                       f.write(";".join(self.liste_entete)+"\n")

		# ledStick
		self.LEDStick = GroveLedStick(12,10)	
		self.numberLedStickLED=-1
		# sound sensor 
		self.soundSensor = GroveSoundSensor(0)
		self.noise = 0 
		# temperature & humidity
		self.DHTSensor = GroveDHTSensor(26)
		self.humidity = 0
		self.temperature = 0
		# buttonLED
		self.bLed1 = GroveButtonLed(6,5)
		self.bLed2 = GroveButtonLed(17,16)  
		# PIR sensor & sa valeur
		self.PIRsensor = GrovePirMotionSensor(18)
		# AirQuality Sensor
		self.AirQualitySensor = GroveAirQualitySensor()
		# Buzzer
		self.BuzzerAlert = GroveBuzzer(22)



	def inputUpdate(self):
		print("Mise à jour des entrées")

		##### Recuperation INPUT des capteurs #####
		# Récupération de la valeur du capteur sonore
		self.noise = self.soundSensor.getRawSensorValue()
		# Récupération de la température & humidity
		self.DHTSensor.getRawSensorValue()
		self.humidity = round(self.DHTSensor.humidity(),2)
		self.temperature = round(self.DHTSensor.temperature(),2) 
		# Récupération valeur PIR sensor
		self.isPeopleDetected = self.PIRsensor.getSensorValue()
		# Récuperation des valeur de Airquality sensor
		self.AirQualitySensor.getRawSensorValue()
		self.TVoC = self.AirQualitySensor.TVoC()
		self.CO2eq = self.AirQualitySensor.CO2eq()
		# Button LED
		self.b1_status = self.bLed1.getStatusButton()
		self.b2_status = self.bLed2.getStatusButton()
		print([self.b1_status,self.b2_status])


		# Récupération statut des boutons
		# print("statu b1 : "+ str(self.bLed1.getStatusButton()))
		# Insertion des données dans le tableau JSON
		self.dico_data_JSON["temperature"]= self.temperature
		self.dico_data_JSON["humidity"]=self.humidity
		self.dico_data_JSON["noise"]=self.noise
		self.dico_data_JSON["isPeopleDetected"]=self.isPeopleDetected
		self.dico_data_JSON["TVoC"]=self.TVoC
		self.dico_data_JSON["CO2eq"]=self.CO2eq

		##### Integration des données des X dernières seconde dans un fichier JSON #####
		# Le but est d'utiliser ce tableau JSON dans la methode self.graphe()
		# (=liste pythonde dictionnaires)
		print(len(self.data_JSON))
		if len(self.data_JSON) ==  20 :
			self.data_JSON.pop(0)

		self.data_JSON.append(self.dico_data_JSON)
		with open("last_data_JSON.json", "w") as f:
			f.write(str(self.data_JSON))
		#print(len(self.data_JSON)) 


		##### Ecriture dans le fichier csv - historique des données  #####
		# On reinitialise la liste d'input pour qu'elle ne contienne 
		# que les valeurs de cette itération
		self.liste_input_CSV = []
		# convertir la valeur de time() renvoyee par python
		self.liste_input_CSV.append(str(datetime.datetime.now()))
		self.liste_input_CSV.append(str(self.temperature))
		self.liste_input_CSV.append(str(self.humidity))
		self.liste_input_CSV.append(str(self.noise))
		self.liste_input_CSV.append(str(self.isPeopleDetected))
		self.liste_input_CSV.append(str(self.TVoC))
		self.liste_input_CSV.append(str(self.CO2eq))
		#print(";".join(self.liste_input))
		with open("all_data.csv", "a") as f:
			f.write(";".join(self.liste_input_CSV)+"\n")

	def inputProcessing(self):
		# adaptation des entrée (modification format)
		print("Traitement des entrées")
		print(self.isPeopleDetected)

		# temperature
		self.moyenne_temperature = self.calcul_moyenne_derniere_sec("temperature")
		# print("moyenne temp : ")
		# print(self.moyenne_temperature)
		# humidity en pourcentage
		self.moyenne_humidity = round(self.calcul_moyenne_derniere_sec("humidity"), 2)
		self.moyenne_CO2eq = self.calcul_moyenne_derniere_sec("CO2eq")
		self.moyenne_TVoC = self.calcul_moyenne_derniere_sec("TVoC")
		print([self.moyenne_humidity, self.CO2eq, self.TVoC])

	def graph(self):
		# scenario + traitement
		print("Graph d'état")

		# appeler script python annexe.


	def outputProcessing(self):
		# adaptation des variables pour les sorties
		print("Traitement des sorties")


		# Modification valeur rgb ledStick en fonction de l'humidity moy.
		# Si inferieur au seuil : vert 
		# sinon : rouge 
		if self.moyenne_CO2eq < 800 :
			self.red_CO2 = int(0)
			self.blue_CO2 = int(0)
			self.green_CO2 = int(160)
		elif self.moyenne_CO2eq < 1500 and self.moyenne_CO2eq >= 800:
			self.red_CO2 = int(255)
			self.blue_CO2 = int(0)
			self.green_CO2 = int(75)
		else :
			self.red_CO2 = int(255)
			self.blue_CO2 = int(0)
			self.green_CO2 = int(0)

		# Modification valeurs rgb en fonction de la temperature moy.
		var_temperature = (19-self.moyenne_temperature)*35
		if var_temperature < 0 :
			self.red_temperature = int(255)
			self.blue_temperature = int(0)
			self.green_temperature = int(255+var_temperature)
			if self.green_temperature < 0 :
				self.green_temperature = 0
		else :
			self.blue_temperature = int(0+var_temperature)
			if self.blue_temperature > 255 :
				self.blue_temperature = int(255)
			self.red_temperature = int(255-var_temperature)
			if self.red_temperature < 0 :
				self.red_temperature = int(0)
			self.green_temperature = int(255)

	def outputUpdate(self):
		print("Traitement des sorties")
		# ecrire dans le ficher csv qui contient toutes nos valeurs 
		# (ou mettre a jour le ficher sur le serveur)
		if self.isPeopleDetected  == 1 :
			self.BuzzerAlert.off()
		else :
			self.BuzzerAlert.off()
		self.LEDStick.LedRGB_ON(0, self.red_temperature, self.green_temperature, self.blue_temperature)

		self.LEDStick.LedRGB_ON(4, self.red_CO2, self.green_CO2, self.blue_CO2)






	# Methode de classe de traitement et formatage de données
	def calcul_moyenne_derniere_sec(self, dico_key:str):
		somme = 0
		for i in range(len(self.data_JSON)) :
			somme += self.data_JSON[i][dico_key]
		moyenne = somme/len(self.data_JSON)
		return (moyenne)

