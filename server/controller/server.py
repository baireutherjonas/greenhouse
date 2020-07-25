import paho.mqtt.client as mqtt
import configparser
import datetime
from decision_maker import decisionMaker
from database_connector import storeData, storeLogging
import logging
import json

config = configparser.ConfigParser()
config.read("config.ini")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(config.get('Topics','TOPIC_SENSOR_DATA'))
    client.subscribe(config.get('Topics','TOPIC_STATUS_MONITOR'))
    client.subscribe(config.get('Topics','TOPIC_RECEIVED_DATA'))
    
    client.message_callback_add(config.get('Topics','TOPIC_SENSOR_DATA'),__callback_sensorData)
    client.message_callback_add(config.get('Topics','TOPIC_STATUS_MONITOR'),__callback_statusMonitor)
    client.message_callback_add(config.get('Topics','TOPIC_RECEIVED_DATA'),__callback_receivedData)

def __callback_sensorData(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    msgJson = json.loads(msg.payload)
    logging.warning("received sensor data: " + str(msgJson))
    # store data into database
    storeData(config,msgJson)

def __callback_statusMonitor(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    print("received status monitor: " + str(msg.payload))
    storeLogging(config, str(msg.payload))
    decisionMaker(msg.payload, config)


def __callback_receivedData(client, userdata, msg):
    print("received data: " + str(msg.payload))
    # store log messages from arduino in database
    storeLogging(config, str(msg.payload))
    
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

client = mqtt.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe

client.connect(config.get("Config", "BROKER"), 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
