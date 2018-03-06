#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os
import paho.mqtt.client as mqtt
from concurrent.futures import ThreadPoolExecutor
import json, time

import psutil

def get_data(mqtt, parametre):
	data = {"value":-1, "name":parametre, "format":""}
	if parametre == "cpu":
		data["value"] = psutil.cpu_percent()
		mqtt.publish("/test/cpu/100", payload=json.dumps(data), qos=2, retain=False)
	
	if parametre == "mem":
		data["value"] = psutil.virtual_memory().percent
		mqtt.publish("/test/mem/101", payload=json.dumps(data), qos=2, retain=False)
	
	if parametre == "disk":
		data["value"] = psutil.disk_usage("/").percent
		mqtt.publish("/test/disk/102", payload=json.dumps(data), qos=2, retain=False)
	

def main():
	data_to_read = ["cpu", "mem", "disk"]
	MQTT = mqtt.Client()
	#MQTT = mqtt.Client(client_id="historian", clean_session=False)
	#MQTT.username_pw_set(username, password=None)
	#MQTT.reconnect_delay_set(min_delay=1, max_delay=30)
	
	#print("Client MQTT pour %s:%s"%(args.mqtt_host, args.mqtt_port))
	#MQTT.connect_async(args.mqtt_host, args.mqtt_port, 60)
	MQTT.connect_async("localhost", 1883, 60)

	MQTT.loop_start()
	
	Pool = ThreadPoolExecutor(max_workers=16)

	while True:
		for i in data_to_read:
			Pool.submit(get_data, MQTT, i)
		time.sleep(30)


	MQTT.loop_stop(force=False)

if __name__ == '__main__':
	main()
