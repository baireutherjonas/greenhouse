// PINS
#define RELAISPIN 2

// WATERING
long startWateringTime;
bool isWatering;

void initWatering() {
  pinMode(RELAISPIN, OUTPUT);
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
