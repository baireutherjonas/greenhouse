import paho.mqtt.publish as publish
import json
import os

def getSensorData():
    msg = {
    "action": os.environ['ACTIONS_ACTION_GET_SENSOR_DATA'],
    "parameter":{"sleppingtime":2,"watergroundDistance":24,"soilMoistureMax":800,"soilMoistureMin":300}
    }

    # convert into JSON:
    msgJSON = json.dumps(msg)
    publish.single(os.environ['TOPICS_TOPIC_ACTION_GREENHOUSE'], msgJSON, hostname=os.environ['CONFIG_BROKER'])
    