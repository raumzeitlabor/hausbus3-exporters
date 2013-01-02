#!/usr/bin/python
# coding=utf8

import mosquitto
import json
import time

broker = "tiefpunkt.vm.rzl"

def on_message(mosq, obj, msg):
	content = json.loads(msg.payload)
	t = time.gmtime(content["_timestamp"])
	for key, value in content.items():
		if key == "_timestamp":
			continue
		print "temperatur "+str(time.strftime("%s",t))+" "+str(value)+" sensor="+key

mqtt = mosquitto.Mosquitto("opentsdb-client", clean_session=False)
mqtt.will_set(topic="/monitor", payload=json.dumps({"event": "unexpected_disconnect","device": "opentsdb-client"}))

mqtt.on_message = on_message

mqtt.connect(broker)

mqtt.subscribe("/device/+/temperature", 2)

mqtt.loop_forever()
