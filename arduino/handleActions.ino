// LIBRARIES
#include <DHT.h>
#include <ArduinoJson.h>

// PINS
#define RELAISPIN 2
#define SOILPIN A0
#define DHTPINOUTDOOR 5
#define DHTPIN 4
#define DHTTYPE DHT22
#define TRIGGERPIN 15
#define ECHOPIN 13

// DHT22
DHT dht(DHTPIN, DHTTYPE);
DHT dht_outdoor(DHTPINOUTDOOR, DHTTYPE);


void initSensorActuators() {
  dht.begin();
  dht_outdoor.begin();
  pinMode(RELAISPIN, OUTPUT);
  pinMode(TRIGGERPIN, OUTPUT);
  pinMode(ECHOPIN, OUTPUT);
}

void startWatering() {
  digitalWrite(RELAISPIN, HIGH);
  publishMessage(TOPIC_STATUS_DATA, MESSAGE_START_WATERING);
}

void stopWatering() {
  digitalWrite(RELAISPIN, LOW);
  publishMessage(TOPIC_STATUS_DATA, MESSAGE_STOP_WATERING);
}

long getWaterstand() {
  digitalWrite(TRIGGERPIN, LOW);
  delay(5);
  digitalWrite(TRIGGERPIN, HIGH);
  delay(10);
  digitalWrite(TRIGGERPIN, LOW);
  long duration = pulseIn(ECHOPIN, HIGH);
  return config_watergroundDistance-(duration/2) * 0.03432;
}

void getSensorData() {
  long waterheight = getWaterstand();
  float hum = dht.readHumidity();
  float temp= dht.readTemperature();
  float hum_outdoor = dht_outdoor.readHumidity();
  float temp_outdoor= dht_outdoor.readTemperature();
  int sensorValue = analogRead(SOILPIN);
  int sensorValueMapped = map(sensorValue,config_soilMoistureMax,config_soilMoistureMin,0,100);
  
  // Prepare JSON document
  DynamicJsonDocument doc(2048);
  doc[JSON_KEY_INDOOR][JSON_KEY_TEMP] = String(temp);
  doc[JSON_KEY_INDOOR][JSON_KEY_HUM] = String(hum);
  doc[JSON_KEY_OUTDOOR][JSON_KEY_TEMP] = String(temp_outdoor);
  doc[JSON_KEY_OUTDOOR][JSON_KEY_HUM] = String(hum_outdoor);
  doc[JSON_KEY_SOIL][JSON_KEY_MOISTURE] = String(sensorValueMapped);
  doc[JSON_KEY_SOIL][JSON_KEY_MOISTURE_RAW] = String(sensorValue);
  doc[JSON_KEY_WATER][JSON_KEY_HEIGHT] = String(waterheight);
  
  // Serialize JSON document
  String json;
  serializeJson(doc, json);

  publishMessage(TOPIC_SENSOR_DATA, json);
}
