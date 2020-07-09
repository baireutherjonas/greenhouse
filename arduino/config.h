#define CLIENT_ID "greenhouse"

#define TOPIC_RECEIVED_DATA "/greenhouse/receivedData"
#define TOPIC_SENSOR_DATA "/greenhouse/sensorData"
#define TOPIC_STATUS_DATA "/greenhouse/statusMonitor"
#define TOPIC_ACTION_GREENHOUSE "/greenhouse/actionGreenhouse"

#define MESSAGE_GREENHOUSE_IS_ONLINE "greenhouse is now connected"
#define MESSAGE_START_WATERING "greenhouse start watering"
#define MESSAGE_STOP_WATERING "greenhouse stop watering"

#define ACTION_START_WATERING ""
#define ACTION_STOP_WATERING ""
#define ACTION_GET_SENSOR_DATA ""

#define JSON_KEY_HUM "hum"
#define JSON_KEY_OUTDOOR "outdoor"
#define JSON_KEY_INDOOR "indoor"
#define JSON_KEY_TEMP "temp"
#define JSON_KEY_SOIL "soil"
#define JSON_KEY_MOISTURE "moisture"
#define JSON_KEY_MOISTURE_RAW "moistureraw"
#define JSON_KEY_WATER "water"
#define JSON_KEY_HEIGHT "height"

const int config_watergroundDistance = 24;
const int config_soilMoistureMax = 800;
const int config_soilMoistureMin = 330;
