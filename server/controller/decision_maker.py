import threading
import time
from actuator_activator import activatePump, sendArduinoToSleep
from collector import getSensorData
import json
import datetime
import os
import redis

def decisionMaker(message, client):
    try:
        print(str(datetime.datetime.now()) + " Decision maker activated")
        msgJson = json.loads(message)

        r = redis.Redis(host=os.environ['CONFIG_REDIS'], port=6379, db=0)

        if 'action' in msgJson:
            if(msgJson['action'] == os.environ['ARDUINOMESSAGES_MESSAGE_GREENHOUSE_IS_ONLINE']):
                print(str(datetime.datetime.now()) + " DM: received message: " + os.environ['ARDUINOMESSAGES_MESSAGE_GREENHOUSE_IS_ONLINE'])
                getSensorData(r)
                print(str(datetime.datetime.now()) + " DM: collect sensor Data")
                now = datetime.datetime.now()
                if( now.hour == int(r.get('pumpingstarthour')) and now.minute <= int(r.get('pumpingduration')) + int(r.get('sleepduration')) - 1):
                    print(str(datetime.datetime.now()) + " DM: action: Start pumping")
                    threading.Thread(target=activatePump, args=[r.get('pumpingduration'),r.get('sleepduration'), client]).start()
                else:
                    print(str(datetime.datetime.now()) + " DM: action: send to sleep")
                    sendArduinoToSleep(r.get('sleepduration'), client)
        else:
            print(str(datetime.datetime.now()) + " DM: action: send to sleep")
            sendArduinoToSleep(r.get('sleepduration'), client)
    except ValueError:
        pass


   