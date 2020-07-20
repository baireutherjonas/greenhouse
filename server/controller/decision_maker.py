import threading
import time
from actuator_activator import activatePump
import json
import datetime
import paho.mqtt.publish as publish

lastPumpDay = 0

def decisionMaker(message, config):
    try:
        msgJson = json.loads(message)
        if 'action' in msgJson:
            if(msgJson['action'] == config.get('ArduinoMessages', 'MESSAGE_GREENHOUSE_IS_ONLINE')):
                now = datetime.datetime.now()
                if( now.hour == int(config.get('Settings','PUMPINGSTARTHOUR')) and now.minute <= int(config.get('Settings','PUMPINGDURATION')) + int(config.get('Settings','SLEEPDURATION')) - 1):
                    threading.Thread(target=activatePump, args=(config.get('Settings','PUMPINGDURATION'), config)).start()
                else:
                    sendArduinoToSleep(config)
        else:
            sendArduinoToSleep(config)
    except ValueError:
        pass

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
   