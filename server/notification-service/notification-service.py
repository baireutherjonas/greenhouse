import paho.mqtt.client as mqtt
from os import path
import json
import subprocess
import os
import redis

class SignalNotificationService():
    """Implement the notification service for Join."""

    def __init__(self, sender_nr, recp_nr, signal_conf_path, signal_cli_path):
        """Initialize the service."""
        self.sender_nr = sender_nr
        self.recp_nr = recp_nr
        self.signal_conf_path = signal_conf_path
        self.signal_cli_path = path.join(signal_cli_path, "signal-cli")

    def send_message(self, message=""):
        """Send a message to a user."""
        mainargs = [self.signal_cli_path]

        mainargs.extend(["--config", self.signal_conf_path])
        

        mainargs.extend(["-u", self.sender_nr, "send"])
        mainargs.extend([self.recp_nr])

        mainargs.extend(["-m", message])

        # Raise an Exception if something goes wrong
        p = subprocess.Popen(mainargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait for completion
        p.wait()
        output, err = p.communicate()
        ret = p.returncode

        if ret != 0:
            raise Exception("Signal Error %d: '%s'" % (ret, err))

def sendMessage(message):
    return signalSender.send_message(message)

def __initSignal(sender, recp, conf_path, cli_path):
    sender_nr = sender
    recp_nr = recp
    signal_cli_path = cli_path
    signal_conf_path = conf_path

    if sender_nr is None or signal_cli_path is None:
        return "Please specify sender_nr and signal_cli_path"
    if recp_nr is None:
        return "recp_nr is required"

    return SignalNotificationService(sender_nr, recp_nr, signal_conf_path, signal_cli_path)


r = redis.Redis(host=os.environ['CONFIG_REDIS'], port=6379, db=0)
signalSender = __initSignal(r.get('signalsender'),r.get('signalreceiver'),os.environ['SIGNAL_CONF_PATH'],os.environ['SIGNAL_CLI_PATH'])

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(str(datetime.datetime.now()) + " Connected with result code "+str(rc))
    client.subscribe(os.environ['TOPICS_TOPIC_NOTIFICATIONS'])  
    client.message_callback_add(os.environ['TOPICS_TOPIC_NOTIFICATIONS'],__callback_notification)
   
   
def __callback_notification(client, userdata, msg):
    print(str(datetime.datetime.now()) + " Send notification: " + str(msg.payload))
    sendMessage( str(msg.payload))
    
def on_subscribe(mosq, obj, mid, granted_qos):
    print(str(datetime.datetime.now()) + " Subscribed: " + str(mid) + " " + str(granted_qos))

client = mqtt.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe

client.connect(os.environ['CONFIG_BROKER'], 1883, 60)

client.loop_forever()