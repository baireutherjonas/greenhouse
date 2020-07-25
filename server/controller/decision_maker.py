import threading
import time
from actuator_activator import activatePump, sendArduinoToSleep
from collector import getSensorData
import json
import datetime
import paho.mqtt.publish as publish
import logging

lastPumpDay = 0

def decisionMaker(message, config):
    try:
        logging.warning("Decision maker activated")
        getSensorData(config)
        msgJson = json.loads(message)
        if 'action' in msgJson:
            if(msgJson['action'] == config.get('ArduinoMessages', 'MESSAGE_GREENHOUSE_IS_ONLINE')):
                logging.warning("Received message: " + config.get('ArduinoMessages', 'MESSAGE_GREENHOUSE_IS_ONLINE'))
                now = datetime.datetime.now()
                if( now.hour == int(config.get('Settings','PUMPINGSTARTHOUR')) and now.minute <= int(config.get('Settings','PUMPINGDURATION')) + int(config.get('Settings','SLEEPDURATION')) - 1):
                    logging.warning("Action: Start pumping")
                    threading.Thread(target=activatePump, args=(config.get('Settings','PUMPINGDURATION'), config)).start()
                else:
                    sendArduinoToSleep(config)
        else:
            sendArduinoToSleep(config)
    except ValueError:
        pass


   