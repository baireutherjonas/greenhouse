import time
import json
import os
import datetime

def activatePump(duration, sleepduration, client):

    msg = {
        "action": os.environ['ACTIONS_ACTION_START_WATERING'],
        "parameter": {
            "duration": int(duration),
            "sleepingtime": int(sleepduration)
        }
    }

    client.publish("/greenhouse/notifications",json.dumps("start watering"))
   
    client.publish(os.environ['TOPICS_TOPIC_ACTION_GREENHOUSE'],json.dumps(msg))
    print(str(datetime.datetime.now()) + " Actuator activator: start pumping")


def sendArduinoToSleep(duration, client):
    msg = {
        "action": os.environ['ACTIONS_ACTION_SLEEP'],
        "parameter": {
            "sleepingtime": int(duration)
        }
    }

    client.publish(os.environ['TOPICS_TOPIC_ACTION_GREENHOUSE'],json.dumps(msg))
    print(str(datetime.datetime.now()) + " Actuator activator: send to sleep for: " + str(duration))
