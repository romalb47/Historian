#!/usr/bin/env python3

import sys, os, logging, argparse
from threading import Thread

import json, sqlite3
import paho.mqtt.client as mqtt

# import interne
import bdd_helper, mqtt_cb, main_struct

import rest_class

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--config", help="Config file path", default="./config.json")
	parser.add_argument("-d", "--debug", help="Debugging mode", action="store_true")
	
	parser.add_argument("-s", "--sql", help="SQL Url", default="sqlite://sql.db")
	
	parser.add_argument("-m", "--mqtt-host", help="MQTT Broker address", default="127.0.0.1")
	parser.add_argument("--mqtt-port", help="MQTT Broker port", type=int, default=1883)
	parser.add_argument("--mqtt-topic", help="MQTT Broker port", type=str, default="/#")
	
	args = parser.parse_args()

	try:
		PARAM = json.load(open(args.config, "r"))
	except:
		PARAM = {}

	MAIN = main_struct.MainClass()

	BDD = bdd_helper.init_bdd(args.sql)

	MQTT = mqtt.Client()
	#MQTT = mqtt.Client(client_id="historian", clean_session=False)
	#MQTT.username_pw_set(username, password=None)
	#MQTT.reconnect_delay_set(min_delay=1, max_delay=30)

	MQTT.on_connect = mqtt_cb.on_connect
	MQTT.on_message = mqtt_cb.on_message
	MQTT.on_disconnect = mqtt_cb.on_disconnect
	
	MQTT.user_data_set(MAIN)
	
	print("Client MQTT pour %s:%s"%(args.mqtt_host, args.mqtt_port))
	MQTT.connect_async(args.mqtt_host, args.mqtt_port, 60)

	MAIN.bdd = BDD
	MAIN.mqtt = MQTT
	MAIN.main_topic = args.mqtt_topic

	rest_class.MainClass = MAIN

	MAIN.mqtt.loop_start()

	# Serveur REST ici

	rest_class.app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)
	

	MAIN.mqtt.loop_stop(force=False)

if __name__ == "__main__":
	main()
