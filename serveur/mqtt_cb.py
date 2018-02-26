#!/usr/bin/env python3

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	print("Connection returned result: "+ mqtt.connack_string(rc))
	client.subscribe(userdata.main_topic, 2)
	
def on_message(client, userdata, message):
	print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))

def on_disconnect(client, userdata, rc=-1):
	print("Disconnected flags"+" result code "+str(rc))
