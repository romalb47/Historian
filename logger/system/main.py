#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os
import paho.mqtt.client as mqtt
import concurrent.futures
import sched, time

import psutil

def get_data(mqtt, parametre):
	psutil.cpu_percent()

def main():	
	MQTT = mqtt.Client()
	#MQTT = mqtt.Client(client_id="historian", clean_session=False)
	#MQTT.username_pw_set(username, password=None)
	#MQTT.reconnect_delay_set(min_delay=1, max_delay=30)
	
	print("Client MQTT pour %s:%s"%(args.mqtt_host, args.mqtt_port))
	MQTT.connect_async(args.mqtt_host, args.mqtt_port, 60)

	MQTT.loop_start()
	
	sch = sched.scheduler(time.time, time.sleep)

	Pool = ThreadPoolExecutor(max_workers=16)

	while True:
		Pool.submit(get_data, MQTT, "cpu")
		Pool.submit(get_data, MQTT, "mem")
		Pool.submit(get_data, MQTT, "net")
		
		time.sleep(5)


	MQTT.loop_stop(force=False)

if __name__ == '__main__':
	main()
