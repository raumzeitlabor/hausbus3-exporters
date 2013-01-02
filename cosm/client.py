#!/usr/bin/python
# coding=utf8

import mosquitto
import json
import time
import eeml
import sys

import config

feed = eeml.Pachube(config.API_URL, config.API_KEY, use_https=False)

def on_message(mosq, obj, msg):
	content = json.loads(msg.payload)
	t = time.gmtime(content["_timestamp"])
	
	update_data = []
	
	for key, value in content.items():
		if key == "_timestamp":
			continue
		update_data.append(eeml.Data(config.datastream[key], value, unit=eeml.Celsius()))
		
	feed.update(update_data)
	try:
		feed.put()
	except Exception, err:
		print >> sys.stderr, "Couldn't send data to pachube: ", err

mqtt = mosquitto.Mosquitto("cosm-client", clean_session=False)
mqtt.will_set(topic="/monitor", payload=json.dumps({"event": "unexpected_disconnect","device": "cosm-client"}))

mqtt.on_message = on_message

mqtt.connect(config.mqtt_broker)

mqtt.subscribe("/device/+/temperature", 2)

mqtt.loop_forever()
