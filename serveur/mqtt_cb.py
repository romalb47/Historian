#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import bdd_helper
import json

def on_connect(client, userdata, flags, rc):
	print("Connection returned result: "+ mqtt.connack_string(rc))
	client.subscribe(userdata.main_topic, 2)
	
def on_message(client, userdata, message):
	bdd = userdata.bdd
	
	data = json.loads(message.payload.decode())
	
	value = data["value"]
	
	idx = bdd_helper.getOrAddIdentifiant(bdd, message.topic, data.get("name", ""), data.get("format", ""))
	
	try:
		bdd_helper.addHistoryData(bdd, idx, value)
		print("Ajout de '" + str(data["value"]) + "' depuis '" + message.topic + "'")
	except:
		print("Erreur d'enregistrement!")
		return

	
	
	
	

def on_disconnect(client, userdata, rc=-1):
	print("Disconnected flags"+" result code "+str(rc))
