import datetime
from django.shortcuts import render, redirect
from app.models import Dispositivo, Sensor, Leitura
from app.forms import DispositivoForm, FiltroLocalizacaoForm, SensorForm
from django.db.models import Avg
from datetime import datetime, timedelta

from django.shortcuts import render
from .models import Leitura

from app.mqtt import publish_message, publish_device_info
from SmartFarm.mqtt import client as mqtt_client

def first(request):
    return render(request, 'first.html')


def home(request):

    overview_localizacoes = []
    overview_leituras = []

    # Processar o formulário de filtro de localização
    form = FiltroLocalizacaoForm(request.GET)
    if form.is_valid():
        localizacao_selecionada = form.cleaned_data['localizacao']
        if localizacao_selecionada:
            dispositivos = Dispositivo.objects.filter(
                localizacao=localizacao_selecionada)
        else:
            dispositivos = Dispositivo.objects.all()

    else:
        dispositivos = Dispositivo.objects.all()

    localizacoes = dispositivos.values_list(
        'localizacao', flat=True).distinct()

    for localizacao in localizacoes:
        dispositivos_localizacao = dispositivos.filter(localizacao=localizacao)

        num_dispositivos = dispositivos_localizacao.count()
        num_sensores = Sensor.objects.filter(
            dispositivo__in=dispositivos_localizacao).count()
        num_sensores_ativos = Sensor.objects.filter(
            dispositivo__in=dispositivos_localizacao, ativo=True).count()

        # Calcula o status do sensor para a localização atual
        if num_sensores_ativos == 0:
            # Nenhum sensor ativo (bolinha vermelha)
            dispositivos_status = 'vermelho'
        elif num_sensores_ativos < num_sensores:
            # Alguns sensores não ativos (bolinha laranja)
            dispositivos_status = 'laranja'
        else:
            # Todos os sensores ativos (bolinha verde)
            dispositivos_status = 'verde'

        overview_localizacoes.append(
            (localizacao, num_dispositivos, num_sensores, f"{num_sensores_ativos}/{num_sensores}", dispositivos_status))

        # Cálculo das médias de temperatura, umidade e pH
        leituras_localizacao = Leitura.objects.filter(
            sensor__dispositivo__in=dispositivos_localizacao)
        media_temperatura = round(leituras_localizacao.filter(sensor__tipo='temperatura').aggregate(
            media=Avg('valor'))['media'], 2)
        media_humidade = round(leituras_localizacao.filter(sensor__tipo='humidade').aggregate(
            media=Avg('valor'))['media'] * 100, 2)
        media_ph = leituras_localizacao.filter(
            sensor__tipo='ph').aggregate(media=Avg('valor'))['media']

        overview_leituras.append((
            localizacao,
            f"{media_temperatura} °C",
            f"{media_humidade} %",
            media_ph,
            verificar_medida(media_temperatura, 25, 10),
            verificar_medida(media_humidade, 50, 10),
            verificar_medida(media_ph, 7, 10)
        ))

    context = {
        'overview_localizacoes': overview_localizacoes,
        'overview_leituras': overview_leituras,
        'localizacoes': localizacoes,
        'form': form,  # Adiciona o formulário de filtro ao contexto
    }
    return render(request, 'home.html', context)


def dispositivos(request):
    dispositivos = Dispositivo.objects.all()

    context = {
        'dispositivos': dispositivos
    }
    return render(request, 'dispositivos_e_sensores.html', context)


def delete_dispositivo(request, dispositivo_id):
    dispositivo = Dispositivo.objects.get(id=dispositivo_id)
    dispositivo.delete()
    return redirect('dispositivos_e_sensores')


def adicionar_dispositivo(request):
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            dispositivo = form.save()
            mqtt_client.subscribe(f'SmartFarm/{dispositivo.id}/read') # Subscribe device read
            return redirect('dispositivos_e_sensores')
    else:
        form = DispositivoForm()

    context = {
        'form': form
    }
    return render(request, 'adicionar_dispositivo.html', context)


def atualizar_dispositivo(request, dispositivo_id):
    dispositivo = Dispositivo.objects.get(id=dispositivo_id)
    if request.method == 'POST':
        form = DispositivoForm(request.POST, instance=dispositivo)
        if form.is_valid():
            form.save()
            return redirect('dispositivos_e_sensores')
    else:
        form = DispositivoForm(instance=dispositivo)

    context = {
        'form': form
    }
    return render(request, 'atualizar_dispositivo.html', context)


def sensores(request):
    sensores = Sensor.objects.all()
    context = {
        'sensores': sensores
    }
    return render(request, 'sensores.html', context)


def delete_sensor(request, sensor_id):
    sensor = Sensor.objects.get(id=sensor_id)
    sensor.delete()
    return redirect('dispositivos_e_sensores')


def adicionar_sensor(request, dispositivo_id):
    dispositivo = Dispositivo.objects.get(id=dispositivo_id)
    print("Adiciona_sensor")
    if request.method == 'POST':
        form = SensorForm(request.POST)
        if form.is_valid():
            sensor = form.save(commit=False)
            sensor.dispositivo = dispositivo
            sensor.save()
            print(f'enviando para SmartFarm/{sensor.id}/ideal: {sensor.valor_ideal}')
            publish_message(f'SmartFarm/{sensor.id}/ideal', sensor.valor_ideal)
            return redirect('dispositivos_e_sensores')
    else:
        form = SensorForm()

    context = {
        'form': form
    }
    return render(request, 'adicionar_sensor.html', context)


def atualizar_sensor(request, sensor_id):
    sensor = Sensor.objects.get(id=sensor_id)
    print("Atualiza_sensor")
    if request.method == 'POST':
        form = SensorForm(request.POST, instance=sensor)
        if form.is_valid():
            form.save()
            publish_device_info(sensor.dispositivo)
            return redirect('dispositivos_e_sensores')
    else:
        form = SensorForm(instance=sensor)

    context = {
        'form': form
    }
    return render(request, 'atualizar_sensor.html', context)


def relatorio(request):

    context = {}
    if request.POST.get("data-inicio") is not None:
        initial_date = request.POST["data-inicio"]
        end_date = request.POST["data-fim"]
        # Erro de datas
        if initial_date == "" or end_date == "" or datetime.strptime(initial_date, "%Y-%m-%d") > datetime.strptime(end_date, "%Y-%m-%d"):
            context["error_msg"] = "Insira datas válidas."
            return render(request, 'relatorio.html', context)

        request.session["initial-date"] = initial_date
        request.session["end-date"] = end_date
        return redirect(f"mostrarelatorio")

    else:
        return render(request, 'relatorio.html', context)


def mostrarelatorio(request):
    initial_date = datetime.strptime(request.session.get("initial-date"), "%Y-%m-%d")
    end_date = datetime.strptime(request.session.get("end-date"), "%Y-%m-%d")
    
    dispositivos = Dispositivo.objects.all()
    localizacoes = dispositivos.values_list('localizacao', flat=True).distinct()
    
    dados = [[localizacao, Leitura.objects.filter(sensor__dispositivo__localizacao=localizacao, data_hora__range=(initial_date, end_date)).order_by('data_hora')] for localizacao in localizacoes]
    
    context = {
        'dados': dados,
    }

    return render(request, 'mostrarelatorio.html', context)


def verificar_medida(medida, valor_ideal, erro_aceitavel):
    try:
        erro_percentual = abs((medida - valor_ideal) / valor_ideal) * 100

        if erro_percentual <= erro_aceitavel:
            return 'green'
        elif erro_percentual > erro_aceitavel and erro_percentual <= 2 * erro_aceitavel:
            return 'orange'
        else:
            return 'red'

    except TypeError:  # return default black
        return 'black'
