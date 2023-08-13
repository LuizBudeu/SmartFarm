from SmartFarm.mqtt import client
from app.models import Sensor, Leitura
from datetime import datetime

unidades = {
    'temperatura': '°C',
    'humidade': '%',
    'ph': ''
}

for sensor in Sensor.objects.all():
    print(f'Subscribing to SmartFarm/{sensor.id}/read...')
    client.subscribe(f'SmartFarm/{sensor.id}/read')

def on_message(mqtt_client, userdata, msg):
   print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
   topic_split = msg.topic.split("/")
   sensor_id = topic_split[1]
   print(topic_split)
   sensor = Sensor.objects.get(id=sensor_id)
   print("vono valor " + str(msg.payload.decode("utf-8")))
   Leitura.objects.create(
        sensor=sensor,
        valor=str(msg.payload.decode("utf-8")),
        unidade_medida=unidades[sensor.tipo],
        data_hora=datetime.now()
    )

client.on_message = on_message

def publish_message(topic, message):
    rc, mid = client.publish(topic, message)
    return rc