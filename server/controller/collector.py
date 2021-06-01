import paho.mqtt.publish as publish
import json
import os
import datetime

def getSensorData(r):
    msg = {
    "action": os.environ['ACTIONS_ACTION_GET_SENSOR_DATA'],
    "parameter":{"watergroundDistance":24,"soilMoistureMax":int(r.get('soilMoistureMax')),"soilMoistureMin":int(r.get('soilMoistureMin'))}
    }

    # convert into JSON:
    msgJSON = json.dumps(msg)
    publish.single(os.environ['TOPICS_TOPIC_ACTION_GREENHOUSE'], msgJSON, hostname=os.environ['CONFIG_BROKER'])
    print(str(datetime.datetime.now()) + " Collector: get data")