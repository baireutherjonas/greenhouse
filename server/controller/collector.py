import paho.mqtt.publish as publish
import json

def getSensorData(config):
    msg = {
    "action": config.get('Actions','ACTION_GET_SENSOR_DATA'),
    "parameter":{"sleppingtime":2,"watergroundDistance":24,"soilMoistureMax":800,"soilMoistureMin":300}
    }

    # convert into JSON:
    msgJSON = json.dumps(msg)
    publish.single(config.get('Topics','TOPIC_ACTION_GREENHOUSE'), msgJSON, hostname=config.get('Config','BROKER'))
    