import paho.mqtt.client as mqtt
import datetime
from decision_maker import decisionMaker
from database_connector import storeData, storeLogging
import logging
import json
import os

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(os.environ['TOPICS_TOPIC_SENSOR_DATA'])
    client.subscribe(os.environ['TOPICS_TOPIC_STATUS_MONITOR'])
    client.subscribe(os.environ['TOPICS_TOPIC_RECEIVED_DATA'])
    
    client.message_callback_add(os.environ['TOPICS_TOPIC_SENSOR_DATA'],__callback_sensorData)
    client.message_callback_add(os.environ['TOPICS_TOPIC_STATUS_MONITOR'],__callback_statusMonitor)
    client.message_callback_add(os.environ['TOPICS_TOPIC_RECEIVED_DATA'],__callback_receivedData)

def __callback_sensorData(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    msgJson = json.loads(msg.payload)
    logging.warning("received sensor data: " + str(msgJson))
    # store data into database
    storeData(msgJson)

def __callback_statusMonitor(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    print("received status monitor: " + str(msg.payload))
    storeLogging(str(msg.payload))
    decisionMaker(msg.payload)


def __callback_receivedData(client, userdata, msg):
    print("received data: " + str(msg.payload))
    # store log messages from arduino in database
    storeLogging(str(msg.payload))
    
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

client = mqtt.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe

client.connect(os.environ['CONFIG_BROKER'], 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
