#!/usr/bin/env python3


def on_connect(client, userdata, flags, rc):
	client.subscribe(userdata.main_topic, 2)
	
def on_message(client, userdata, message):
	pass
