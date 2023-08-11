import os
import sys
import django
from pathlib import Path
from datetime import datetime, timedelta
import random


def django_setup():

    # projeto_dir = r'C:\\Users\\itigo\Documents\\VscodePessoal\\Poli\\LabRedes\SmartFarm'
    # projeto_dir = r'D:\\User\\VS_Code_testes\\python\\Poli\\LabRedes\SmartFarm'

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    sys.path.append(str(BASE_DIR))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartFarm.settings")

    django.setup()


def truncate_tables():
    from app.models import Sensor, Dispositivo, Leitura

    print('Truncando tabelas...')
    Leitura.objects.all().delete()
    print('Tabelas truncadas.')


def create_leituras():
    from app.models import Sensor, Dispositivo, Leitura

    print("Criando leituras...")
    # Criar algumas leituras dummy
    # Supondo que o sensor de ID 1 já existe
    sensor_1 = Sensor.objects.all()[:1].get()  # temperatura
    # Supondo que o sensor de ID 2 já existe
    sensor_2 = Sensor.objects.all()[1:2].get()  # humidade

    sensores = Sensor.objects.all()

    valores = {
        'temperatura': (20, 30),
        'humidade': (0.1, 0.9),
        'ph': (1, 14)
    }

    unidades = {
        'temperatura': '°C',
        'humidade': '%',
        'ph': ''
    }

    for i, sensor in enumerate(sensores):
        for j in range(3):
            Leitura.objects.create(
                sensor=sensor,
                valor=random.randint(
                    valores[sensor.tipo][0], valores[sensor.tipo][1]) if type(valores[sensor.tipo][0]) is int else
                random.uniform(
                    valores[sensor.tipo][0], valores[sensor.tipo][1]),
                unidade_medida=unidades[sensor.tipo],
                data_hora=datetime.now() - timedelta(minutes=random.randint(1, 60))
            )

    # # Criar leituras para o sensor 1
    # Leitura.objects.create(
    #     sensor=sensor_1,
    #     valor=25.5,
    #     unidade_medida='°C',
    #     data_hora=datetime(2023, 7, 14, 12, 0, 0)
    # )
    # Leitura.objects.create(
    #     sensor=sensor_1,
    #     valor=80,
    #     unidade_medida='%',
    #     data_hora=datetime(2023, 7, 14, 12, 15, 0)
    # )

    # # Criar leituras para o sensor 2
    # Leitura.objects.create(
    #     sensor=sensor_2,
    #     valor=100,
    #     unidade_medida='lx',
    #     data_hora=datetime(2023, 7, 14, 12, 30, 0)
    # )
    # Leitura.objects.create(
    #     sensor=sensor_2,
    #     valor=10,
    #     unidade_medida='°C',
    #     data_hora=datetime(2023, 7, 14, 12, 45, 0)
    # )
    print("Leituras criadas.")


def main():
    truncate_tables()
    create_leituras()


if __name__ == '__main__':
    django_setup()

    from app.models import Sensor, Dispositivo, Leitura
    main()
