from SmartFarm.mqtt import client
from app.models import Dispositivo, Sensor, Leitura
from datetime import datetime
import json

unidades = {
    'temperatura': '°C',
    'humidade': '%',
    'ph': ''
}

for dispositivo in Dispositivo.objects.all():
    print(f'Subscribing to SmartFarm/{dispositivo.id}/read...')
    client.subscribe(f'SmartFarm/{dispositivo.id}/read')

def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    topic_split = msg.topic.split("/")
    if len(topic_split) == 2:
        print("Recebeu mensagem de conexão")
        print("Id do dispositivo: " + msg.payload.decode("utf-8"))
        device_id = msg.payload.decode("utf-8")
        device = None
        if Dispositivo.objects.filter(id=device_id).exists():
            print("Dispositivo já existe")
            device = Dispositivo.objects.get(id=device_id)
        else:
            print("Dispositivo ainda não existe")
            # Cria dispositivo
            device = Dispositivo.objects.create(
                id=device_id,
                modelo='TelosB',
                localizacao='Setor A',
            )
            # Cria sensores
            Sensor.objects.create(
                modelo='DHT11',
                tipo='temperatura',
                ativo=True,
                valor_ideal=25,
                dispositivo=device,
            )
            Sensor.objects.create(
                modelo='DHT11',
                tipo='humidade',
                ativo=True,
                valor_ideal=50,
                dispositivo=device,
            )
            Sensor.objects.create(
                modelo='Ph4502c',
                tipo='ph',
                ativo=True,
                valor_ideal=7,
                dispositivo=device,
            )

            # Subscribe
            mqtt_client.subscribe(f'SmartFarm/{device_id}/read')
        # Envia valores ideais do dispositivo
        publish_device_info(device)

    elif len(topic_split) == 3:
        print("Recebeu mensagem de informação")
        # Busca sensor
        device_id = topic_split[1]
        print(topic_split)
        dispositivo = Dispositivo.objects.get(id=device_id)

        # Converte string para JSON
        print("nono valor: " + msg.payload.decode("utf-8"))
        json_object = json.loads(msg.payload.decode("utf-8"))
        print(json_object)

        # Grava temperatura
        print("Atualiza temperatura: " + str(json_object["temperatura"]))
        sensor = Sensor.objects.get(dispositivo=dispositivo, tipo="temperatura")
        Leitura.objects.create(
            sensor=sensor,
            valor=str(json_object["temperatura"]),
            unidade_medida=unidades[sensor.tipo],
            data_hora=datetime.now()
        )

        # Grava humidade
        print("Atualiza humidade: " + str(json_object["umidade"]))
        sensor = Sensor.objects.get(dispositivo=dispositivo, tipo="humidade")
        Leitura.objects.create(
            sensor=sensor,
            valor=str(json_object["umidade"]/100),
            unidade_medida=unidades[sensor.tipo],
            data_hora=datetime.now()
        )

        # Grava ph
        print("Atualiza ph: " + str(json_object["ph"]))
        sensor = Sensor.objects.get(dispositivo=dispositivo, tipo="ph")
        Leitura.objects.create(
            sensor=sensor,
            valor=str(json_object["ph"]),
            unidade_medida=unidades[sensor.tipo],
            data_hora=datetime.now()
        )

client.on_message = on_message

def publish_message(topic, message):
    rc, mid = client.publish(topic, message)
    return rc

def publish_device_info(device):
    print(f'Publicando para device {device.id}')

    sensor_temperatura = Sensor.objects.get(dispositivo=device, tipo="temperatura")
    sensor_umidade = Sensor.objects.get(dispositivo=device, tipo="humidade")
    sensor_ph = Sensor.objects.get(dispositivo=device, tipo="ph")

    print(sensor_temperatura.valor_ideal)
    print(sensor_umidade.valor_ideal)
    print(sensor_ph.valor_ideal)

    json_string_msg = f'{int(sensor_umidade.valor_ideal)},{int(sensor_temperatura.valor_ideal)},{int(sensor_ph.valor_ideal)}'
    print(json_string_msg)

    publish_message(f'SmartFarm/{device.id}/ideal', json_string_msg)