// PINS
#define RELAISPIN 2

// WATERING
long startWateringTime;
bool isWatering;

void initWatering() {
  pinMode(RELAISPIN, OUTPUT);
  digitalWrite(RELAISPIN, LOW);
  isWatering = false;  
}

void startWatering(JsonObject jsonObj) {
  publishMessage(TOPIC_STATUS_DATA, MESSAGE_START_WATERING);
  wifi_off();
  digitalWrite(RELAISPIN, HIGH);
  startWateringTime = millis();
  isWatering = true;
  int timeToWatering = jsonObj[JSON_KEY_PARAMETER][JSON_KEY_TIMETOWATERING];
  timeToWatering = timeToWatering * 60000;
  delay(timeToWatering);
  digitalWrite(RELAISPIN, LOW);
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
      publishMessage(TOPIC_STATUS_DATA, MESSAGE_FALLBACK_WATERING);
      stopWatering();
    }
  }
}
