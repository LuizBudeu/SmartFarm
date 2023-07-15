from django.shortcuts import render, redirect
from app.models import Dispositivo, Sensor, Leitura
from app.forms import DispositivoForm, SensorForm


def first(request):
    return render(request, 'first.html')


def home(request):
    return render(request, 'home.html')


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
