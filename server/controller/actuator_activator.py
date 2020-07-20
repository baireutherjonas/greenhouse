import paho.mqtt.publish as publish
import time

def activatePump( duration, config):
    publish.single(config.get('Topics','TOPIC_ACTION_GREENHOUSE'), config.get('Actions','ACTION_START_WATERING'), hostname=config.get('Config','BROKER'))
    time.sleep(duration)
    publish.single(config.get('Topics','TOPIC_ACTION_GREENHOUSE'), config.get('Actions','ACTION_STOP_WATERING'), hostname=config.get('Config','BROKER'))
    decision_maker.sendArduinoToSleep()
    