import time
from gateway_test import gateway

print("Initialisation de l'application")
passerelleObject = gateway.Gateway()
print("Lancement de l'application")

while True:
	print("---------------")
	passerelleObject.inputUpdate()
	passerelleObject.inputProcessing()
	passerelleObject.graph()
	passerelleObject.outputProcessing()
	passerelleObject.outputUpdate()
