import paho.mqtt.publish as publish
import time
import json
import os

def activatePump( duration):

    msg = {
    "action": os.environ['ACTIONS_ACTION_START_WATERING']
    }

    # convert into JSON:
    msgJSON = json.dumps(msg)
    publish.single(os.environ['TOPICS_TOPIC_ACTION_GREENHOUSE'], msgJSON, hostname=os.environ['CONFIG_BROKER'])
    time.sleep(int(duration)*60)

    msg = {
    "action": os.environ['ACTIONS_ACTION_STOP_WATERING']
    }

    # convert into JSON:
    msgJSON = json.dumps(msg)
    publish.single(os.environ['TOPICS_TOPIC_ACTION_GREENHOUSE'], msgJSON, hostname=os.environ['CONFIG_BROKER'])
    sendArduinoToSleep()
    


def sendArduinoToSleep():
    # create json
    # a Python object (dict):
    msg = {
    "action": os.environ['ACTIONS_ACTION_SLEEP'],
    "parameter": {
        "sleepingtime": os.environ['SETTINGS_SLEEPDURATION']
    }
    }

    # convert into JSON:
    msgJSON = json.dumps(msg)

    publish.single(os.environ['TOPICS_TOPIC_ACTION_GREENHOUSE'], msgJSON, hostname=os.environ['CONFIG_BROKER'])
