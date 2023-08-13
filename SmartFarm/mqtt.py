import paho.mqtt.client as mqtt
from . import settings

def on_connect(mqtt_client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe('SmartFarm/basic')
   else:
       print('Bad connection. Code:', rc)

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)