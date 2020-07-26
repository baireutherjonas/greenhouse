import threading
import time
from actuator_activator import activatePump, sendArduinoToSleep
from collector import getSensorData
import json
import datetime
import paho.mqtt.publish as publish
import logging
import os

lastPumpDay = 0

def decisionMaker(message):
    try:
        logging.warning("Decision maker activated")
        getSensorData()
        msgJson = json.loads(message)
        if 'action' in msgJson:
            if(msgJson['action'] == os.environ['ArduinoMessages_MESSAGE_GREENHOUSE_IS_ONLINE']):
                logging.warning("Received message: " + os.environ['ArduinoMessages_MESSAGE_GREENHOUSE_IS_ONLINE'])
                now = datetime.datetime.now()
                if( now.hour == int(os.environ['SETTINGS_PUMPINGSTARTHOUR']) and now.minute <= int(os.environ['SETTINGS_PUMPINGDURATION']) + int(os.environ['SETTINGS_SLEEPDURATION']) - 1):
                    logging.warning("Action: Start pumping")
                    threading.Thread(target=activatePump, args=(os.environ['SETTINGS_PUMPINGDURATION'])).start()
                else:
                    sendArduinoToSleep()
        else:
            sendArduinoToSleep()
    except ValueError:
        pass


   