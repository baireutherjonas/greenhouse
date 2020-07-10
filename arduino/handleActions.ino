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

// WATERING
long startWateringTime;
bool isWatering;

void initSensorActuators() {
  dht.begin();
  dht_outdoor.begin();
  pinMode(RELAISPIN, OUTPUT);
  pinMode(TRIGGERPIN, OUTPUT);
  pinMode(ECHOPIN, OUTPUT);
  isWatering = false;
}

void startWatering(JsonObject jsonObj) {
  digitalWrite(RELAISPIN, HIGH);
  publishMessage(TOPIC_STATUS_DATA, MESSAGE_START_WATERING);
  startWateringTime = millis();
  isWatering = true;
}

void stopWatering() {
  digitalWrite(RELAISPIN, LOW);
  isWatering = false;
  publishMessage(TOPIC_STATUS_DATA, MESSAGE_STOP_WATERING);
}

void __checkFallBackWatering() {
  if(isWatering) {
    long actualTime = millis();
    // 60000 is the minutes to millis factor
    if(actualTime > startWateringTime + config_fallbackMaxWateringDuration* 60000) { 
      stopWatering();
    }
  }
}

long __getWaterstand(int watergroundDistance) {
  digitalWrite(TRIGGERPIN, LOW);
  delay(5);
  digitalWrite(TRIGGERPIN, HIGH);
  delay(10);
  digitalWrite(TRIGGERPIN, LOW);
  long duration = pulseIn(ECHOPIN, HIGH);
  return watergroundDistance-(duration/2) * 0.03432;
}

void getSensorData(JsonObject jsonObj) {
  Serial.println("getsensordata: " );
  long waterheight = __getWaterstand(jsonObj[JSON_KEY_WATERGROUNDDISTANCE]);
  float hum = dht.readHumidity();
  float temp= dht.readTemperature();
  float hum_outdoor = dht_outdoor.readHumidity();
  float temp_outdoor= dht_outdoor.readTemperature();
  int sensorValue = analogRead(SOILPIN);
  int sensorValueMapped = map(sensorValue,jsonObj[JSON_KEY_SOILMOISTUREMAX],jsonObj[JSON_KEY_SOILMOISTUREMIN],0,100);
  
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
  Serial.println("getsensordata: " + json);

  publishMessage(TOPIC_SENSOR_DATA, json);
}

void goSleeping(JsonObject jsonObj) {
  int timeToSleep = jsonObj[JSON_KEY_TIMETOSLEEP];
  ESP.deepSleep(timeToSleep*60000000); 
}
