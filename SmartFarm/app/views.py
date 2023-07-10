from django.shortcuts import render, redirect
from app.models import Dispositivo, Sensor, Leitura
from app.forms import DispositivoForm


def first(request):
    return render(request, 'first.html')

def home(request):
    return render(request, 'home.html')

def dispositivos(request):
    dispositivos = Dispositivo.objects.all()

    context = {
        'dispositivos': dispositivos
    }
    return render(request, 'dispositivos.html', context)

def delete_dispositivo(request, dispositivo_id):
    dispositivo = Dispositivo.objects.get(id=dispositivo_id)
    dispositivo.delete()
    return redirect('dispositivos')

def adicionar_dispositivo(request):
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispositivos')
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
            return redirect('dispositivos')
    else:
        form = DispositivoForm(instance=dispositivo)
    
    context = {
        'form': form
    }
    return render(request, 'atualizar_dispositivo.html', context)


def sensores(request):
    context = {}
    return render(request, 'sensores.html', context)

def relatorio(request):
    context = {}
    return render(request, 'relatorio.html', context)

