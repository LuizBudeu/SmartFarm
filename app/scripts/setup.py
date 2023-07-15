import os
import sys
import django
from pathlib import Path
from setup_dispositivos_sensores import main as main_dispositivos_sensores
from setup_leituras import main as main_leituras


def django_setup():

    # projeto_dir = r'C:\\Users\\itigo\Documents\\VscodePessoal\\Poli\\LabRedes\SmartFarm'
    # projeto_dir = r'D:\\User\\VS_Code_testes\\python\\Poli\\LabRedes\SmartFarm'

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    sys.path.append(str(BASE_DIR))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartFarm.settings")

    django.setup()


if __name__ == '__main__':
    django_setup()

    from app.models import Sensor, Dispositivo, Leitura

    main_dispositivos_sensores()
    main_leituras()
