from django.shortcuts import render, redirect
from app.models import Dispositivo, Sensor, Leitura
from app.forms import DispositivoForm, FiltroLocalizacaoForm, SensorForm


def first(request):
    return render(request, 'first.html')


def home(request):
    localizacoes = Dispositivo.objects.values_list(
        'localizacao', flat=True).distinct()
    overview_localizacoes = []

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

    for localizacao in localizacoes:
        dispositivos_localizacao = dispositivos.filter(localizacao=localizacao)
        num_dispositivos = dispositivos_localizacao.count()
        num_sensores = Sensor.objects.filter(
            dispositivo__in=dispositivos_localizacao).count()
        num_sensores_ativos = Sensor.objects.filter(
            dispositivo__in=dispositivos_localizacao, ativo=True).count()

        # Calcula o status do sensor para a localização atual
        if num_sensores_ativos == 0:
            status = 'vermelho'  # Nenhum sensor ativo (bolinha vermelha)
        elif num_sensores_ativos < num_sensores:
            status = 'laranja'  # Alguns sensores não ativos (bolinha laranja)
        else:
            status = 'verde'  # Todos os sensores ativos (bolinha verde)

        overview_localizacoes.append(
            (localizacao, num_dispositivos, num_sensores, f"{num_sensores_ativos}/{num_sensores}", status))

    context = {
        'overview_localizacoes': overview_localizacoes,
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
            form.save()
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
    if request.method == 'POST':
        form = SensorForm(request.POST)
        if form.is_valid():
            sensor = form.save(commit=False)
            sensor.dispositivo = dispositivo
            sensor.save()
            return redirect('dispositivos_e_sensores')
    else:
        form = SensorForm()

    context = {
        'form': form
    }
    return render(request, 'adicionar_sensor.html', context)


def atualizar_sensor(request, sensor_id):
    sensor = Sensor.objects.get(id=sensor_id)
    if request.method == 'POST':
        form = SensorForm(request.POST, instance=sensor)
        if form.is_valid():
            form.save()
            return redirect('dispositivos_e_sensores')
    else:
        form = SensorForm(instance=sensor)

    context = {
        'form': form
    }
    return render(request, 'atualizar_sensor.html', context)


def relatorio(request):
    context = {}
    return render(request, 'relatorio.html', context)
