import paho.mqtt.publish as publish
import time
import json

def activatePump( duration, config):

    msg = {
    "action": config.get('Actions','ACTION_START_WATERING')
    }

    # convert into JSON:
    msgJSON = json.dumps(msg)
    publish.single(config.get('Topics','TOPIC_ACTION_GREENHOUSE'), msgJSON, hostname=config.get('Config','BROKER'))
    time.sleep(int(duration)*60)

    msg = {
    "action": config.get('Actions','ACTION_STOP_WATERING')
    }

    # convert into JSON:
    msgJSON = json.dumps(msg)
    publish.single(config.get('Topics','TOPIC_ACTION_GREENHOUSE'), msgJSON, hostname=config.get('Config','BROKER'))
    sendArduinoToSleep(config)
    


def sendArduinoToSleep(config):
    # create json
    # a Python object (dict):
    msg = {
    "action": config.get('Actions','ACTION_SLEEP'),
    "parameter": {
        "sleepingtime": config.get('Settings','SLEEPDURATION')
    }
    }

    # convert into JSON:
    msgJSON = json.dumps(msg)

    publish.single(config.get('Topics','TOPIC_ACTION_GREENHOUSE'), msgJSON, hostname=config.get('Config','BROKER'))
