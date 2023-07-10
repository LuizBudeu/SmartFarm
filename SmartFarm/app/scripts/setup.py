import os, sys
import django


def django_setup():

    projeto_dir = r'C:\\Users\\itigo\Documents\\VscodePessoal\\Poli\\LabRedes\SmartFarm\SmartFarm'
    sys.path.append(projeto_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartFarm.settings")

    django.setup()


def truncate_tables():
    print('Truncando tabelas...')
    Sensor.objects.all().delete()
    Dispositivo.objects.all().delete()
    Leitura.objects.all().delete()
    print('Tabelas truncadas.')


def create_objects():
    print('Criando tabelas...')
    d1 = Dispositivo.objects.create(
        modelo='TelosB',
        localizacao='Setor A',
    )
    d2 = Dispositivo.objects.create(
        modelo='TelosB',
        localizacao='Setor A',
    )
    d3 = Dispositivo.objects.create(
        modelo='TelosB',
        localizacao='Setor B',
    )
    d4 = Dispositivo.objects.create(
        modelo='TelosB',
        localizacao='Setor C',
    )

    s = Sensor.objects.create(
        modelo='DHT11',
        tipo='Temperatura',
        ativo=True,
        dispositivo=d1,
    )
    s = Sensor.objects.create(
        modelo='Ph4502c',
        tipo='pH',
        ativo=True,
        dispositivo=d1,
    )
    s = Sensor.objects.create(
        modelo='DHT11',
        tipo='Temperatura',
        ativo=True,
        dispositivo=d2,
    )
    s = Sensor.objects.create(
        modelo='DHT11',
        tipo='Temperatura',
        ativo=True,
        dispositivo=d3,
    )
    s = Sensor.objects.create(
        modelo='DHT11',
        ativo=True,
        dispositivo=d4,
    )

    print(d1.sensores.all())
    print('Tabelas criadas.')



def main():
    truncate_tables()  # ATENCAO!!!
    create_objects()


if __name__ == '__main__':
    django_setup()

    from app.models import Sensor, Dispositivo, Leitura
    main()
