
// LIBRARIES
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "config.h"
#include "wificonfig.h"

// WIFI-CONFIG
WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {
  initWatering();
  Serial.begin(115200);
  setup_wifi();
  client.setServer(MQTT_BROKER, 1883);
  client.setCallback(callback);
  initSensors();
}

void callback(char* topic, byte* payload, unsigned int length) {
  char msg[length];
  for (int i = 0; i < length; i++) {
    msg[i] = (char)payload[i];
  }
  String sTopic = topic;
  String sMsg = msg;
  String sAll = sTopic + ":" + sMsg;

  Serial.println(msg);
  publishMessage(TOPIC_RECEIVED_DATA, sAll);

  // Create json-object out of message
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, sMsg);
  JsonObject jsonObj = doc.as<JsonObject>();
  
  handleMessage(jsonObj);
}

void handleMessage(JsonObject message) {
  const char* error = message[JSON_KEY_ACTION];
  Serial.println(error);
  if(message[JSON_KEY_ACTION] == ACTION_START_WATERING) {
    startWatering(message);
    setup_wifi();
    goSleeping(message);
  } else if(message[JSON_KEY_ACTION] == ACTION_STOP_WATERING) {
    stopWatering();
  } else if(message[JSON_KEY_ACTION] == ACTION_GET_SENSOR_DATA) {
    getSensorData(message);
  } else if(message[JSON_KEY_ACTION] == ACTION_SLEEP) {
    goSleeping(message);
  }
}
 
void setup_wifi() {
    Serial.println("start connecting");
    delay(10); 
    WiFi.begin(SSID, PSK);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("next try");
    }
    Serial.println("connected");
}

void wifi_off() {
  Serial.println("WiFi Off");
  client.disconnect();
  WiFi.disconnect();
  WiFi.mode(WIFI_OFF); 
  WiFi.forceSleepBegin();
}

void publishMessage(char* topic, String message) {
  String msg = message;
  char c[msg.length()+1];
  msg.toCharArray(c, sizeof(c));
  client.publish(topic, c);
}
 
void reconnect() {
  while (!client.connected()) {
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
  __checkFallBackWatering();
}
