#!/usr/bin/env python3

import sys, os, logging, argparse
from threading import Thread

import json, sqlite3
import paho.mqtt.client as mqtt

# import interne
import bdd, mqtt_cb, main_struct

import rest_class

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--config", help="Config file path", default="./config.json")
	parser.add_argument("-d", "--debug", help="Debugging mode", action="store_true")
	
	parser.add_argument("-s", "--sql", help="SQL Url", default="sqlite://:memory:")
	
	parser.add_argument("-m", "--mqtt-host", help="MQTT Broker address", default="127.0.0.1")
	parser.add_argument("--mqtt-port", help="MQTT Broker port", type=int, default=1883)
	parser.add_argument("--mqtt-topic", help="MQTT Broker port", type=str, default="/#")
	
	args = parser.parse_args()

	try:
		PARAM = json.load(open(args.config, "r"))
	except:
		PARAM = {}

	MAIN = main_struct.MainClass()

	BDD = bdd.init_bdd(args.sql)

	MQTT = mqtt.Client(client_id="Historian", clean_session=False, userdata=None)
	#MQTT.username_pw_set(username, password=None)
	MQTT.reconnect_delay_set(min_delay=1, max_delay=30)

	MQTT.on_connect = mqtt_cb.on_connect
	MQTT.on_message = mqtt_cb.on_message
	MQTT.user_data_set(MAIN)
	
	MQTT.connect_async(args.mqtt_host, port=args.mqtt_port, keepalive=60)

	MAIN.bdd = BDD
	MAIN.mqtt = MQTT
	MAIN.main_topic = args.mqtt_topic

	rest_class.MainClass = MAIN

	MQTT.loop_start()

	# Serveur REST ici

	rest_class.app.run(debug=True)
	
	MQTT.loop_stop(force=False)

if __name__ == "__main__":
	main()
