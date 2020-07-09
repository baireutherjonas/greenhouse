#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "config.h"
#include "wificonfig.h"

WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(MQTT_BROKER, 1883);
    client.setCallback(callback);
    initSensorActuators();
}

void callback(char* topic, byte* payload, unsigned int length) {
    char msg[length+1];
    for (int i = 0; i < length+1; i++) {
        msg[i] = (char)payload[i];
    }
    String sTopic = topic;
    String sMsg = msg;
    String sAll = sTopic + ":" + sMsg;
    
    char cMsg[sAll.length()+1];
    sAll.toCharArray(cMsg, sizeof(cMsg));
    publishMessage(TOPIC_RECEIVED_DATA, cMsg);
    handleMessage(msg);
}

void handleMessage(char* message) {
   if(message == ACTION_START_WATERING) {
        startWatering();
    } else if(message == ACTION_STOP_WATERING) {
        stopWatering();
    } else if(message == ACTION_GET_SENSOR_DATA) {
        getSensorData();
    }
}
 
void setup_wifi() {
    delay(10); 
    WiFi.begin(SSID, PSK);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
}

void publishMessage(char* topic, String message) {
  String msg = "received message: " + message;
  char c[msg.length()+1];
  msg.toCharArray(c, sizeof(c));
  client.publish(topic, c);
}
 
void reconnect() {
    while (!client.connected()) {
        //if (!client.connect(CLIENT_ID,NULL, NULL,NULL,1,ACTION_GREENHOUSE_TOPIC,NULL, true)) { for retain messages
        if (!client.connect(CLIENT_ID)) {
            delay(5000);
        }
    }
    client.subscribe(TOPIC_ACTION_GREENHOUSE,1);

    publishMessage(TOPIC_STATUS_DATA, MESSAGE_GREENHOUSE_IS_ONLINE);
}
void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    checkFallBackWatering();
}
