#!/usr/bin/python
# coding=utf8

import os, sys
original_path = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
sys.path.append(original_path)

import mosquitto
import json
import time

broker = "tiefpunkt.vm.rzl"

def on_message(mosq, obj, msg):
	if msg.payload != None:
		try:
			content = json.loads(msg.payload)
			t = content["_timestamp"]
			for key, value in content.items():
				if key == "_timestamp":
					continue
				print "temperatur "+str(t)+" "+str(value)+" sensor="+key
		except Exception, err:
			print >> sys.stderr, "Error:", err

mqtt = mosquitto.Mosquitto("opentsdb-client", clean_session=False)
mqtt.will_set(topic="/monitor", payload=json.dumps({"event": "unexpected_disconnect","device": "opentsdb-client"}))

mqtt.on_message = on_message

mqtt.connect(broker)

mqtt.subscribe("/device/+/temperature", 2)

mqtt.loop_forever()
