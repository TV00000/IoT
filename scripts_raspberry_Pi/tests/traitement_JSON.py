import json

class Traitement() :
	def __init__(self) :
		f = open("last_data_JSON.JSON", "r")
		tableau_JSON = f.readline()
		print(tableau_JSON)
		print(json.loads(tableau_JSON))
		#print(tableau_JSON.split(','))
		# transformer la chaine de caractère en list(dict())
		# Faire des traitements dessus comme :
		#	- caculer la température moyenne sur toutes les input
		#	- définir une variable qui change d'état si le seuil
		#	de CO2 eq détecté est dangereux (trop grand) =>
		#	il faut aérer !
traitement = Traitement()
