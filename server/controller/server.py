import paho.mqtt.client as mqtt
import datetime
from decision_maker import decisionMaker
from database_connector import storeData, storeLogging
from actuator_activator import sendArduinoToSleep
import json
import os
import redis

class Controller():

    def __init__(self, client):
        self.__init_redis()
        self.client = client

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print(str(datetime.datetime.now()) + " Connected with result code "+str(rc))

        client.subscribe(os.environ['TOPICS_TOPIC_SENSOR_DATA'])
        client.subscribe(os.environ['TOPICS_TOPIC_STATUS_MONITOR'])
        client.subscribe(os.environ['TOPICS_TOPIC_RECEIVED_DATA'])
        
        client.message_callback_add(os.environ['TOPICS_TOPIC_SENSOR_DATA'],self.__callback_sensorData)
        client.message_callback_add(os.environ['TOPICS_TOPIC_STATUS_MONITOR'],self.__callback_statusMonitor)
        client.message_callback_add(os.environ['TOPICS_TOPIC_RECEIVED_DATA'],self.__callback_receivedData)

        # initial send arduino to sleep, if he wokes up between container recreation
        #sendArduinoToSleep(r.get('sleepduration'), self.client)


    def __callback_sensorData(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        msgJson = json.loads(msg.payload)
        print(str(datetime.datetime.now()) + " Contoller: received sensor data: " + str(msgJson))
        # store data into database
        storeData(msgJson)
        r = redis.Redis(host=os.environ['CONFIG_REDIS'], port=6379, db=0)

    def __callback_statusMonitor(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        print(str(datetime.datetime.now()) + " Contoller: received status monitor: " + str(msg.payload))
        storeLogging(os.environ['TOPICS_TOPIC_STATUS_MONITOR'], str(msg.payload))
        decisionMaker(msg.payload, self.client)

    def __callback_receivedData(self, client, userdata, msg):
        print(str(datetime.datetime.now()) + " Contoller: received data: " + str(msg.payload))
        # store log messages from arduino in database
        storeLogging(os.environ['TOPICS_TOPIC_RECEIVED_DATA'], str(msg.payload))
        
    def on_subscribe(self, mosq, obj, mid, granted_qos):
        print(str(datetime.datetime.now()) + " Subscribed: " + str(mid) + " " + str(granted_qos))
    
    def on_message(self, client, userdata, message):
        print(str(datetime.datetime.now()) + " Received message in on_message: " + str(message.payload))

    def __init_redis(self):
        r = redis.Redis(host=os.environ['CONFIG_REDIS'], port=6379, db=0)
        if r.get('sleepduration') == None:
            r.set('sleepduration','20')
            r.set('pumpingstarthour','20')
            r.set('pumpingduration','20')
            r.set('signalsender','0')
            r.set('signalreceiver','0')
            r.set('soilMoistureMin','440')
            r.set('soilMoistureMax','940')


if __name__ == '__main__':
    print(str(datetime.datetime.now()) + " Start controller")

    client = mqtt.Client(client_id="controller", clean_session=True)

    controller = Controller(client)

    client.on_connect = controller.on_connect
    client.on_subscribe = controller.on_subscribe
    client.on_message = controller.on_message

    client.connect(os.environ['CONFIG_BROKER'], 1883, 60)

    client.loop_forever()
