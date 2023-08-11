import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from .forms import RelatorioForm
from django.shortcuts import render, redirect
from app.models import Dispositivo, Sensor, Leitura
from app.forms import DispositivoForm, FiltroLocalizacaoForm, SensorForm
from django.db.models import Avg
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse
from .models import Leitura
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import io


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
        media_temperatura = leituras_localizacao.filter(sensor__tipo='temperatura').aggregate(
            media=Avg('valor'))['media']
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
    initial_date = datetime.strptime(
        request.session.get("initial-date"), "%Y-%m-%d")
    end_date = datetime.strptime(request.session.get("end-date"), "%Y-%m-%d")
    localizacao = 'Setor A'  # Substitua pela localização selecionada pelo usuário

    leituras_temperatura = Leitura.objects.filter(
        sensor__dispositivo__localizacao=localizacao,
        data_hora__range=(initial_date, end_date)
    ).order_by('data_hora')

    leituras_humidade = Leitura.objects.filter(
        sensor__dispositivo__localizacao=localizacao,
        data_hora__range=(initial_date, end_date)
    ).order_by('data_hora')

    leituras_ph = Leitura.objects.filter(
        sensor__dispositivo__localizacao=localizacao,
        data_hora__range=(initial_date, end_date)
    ).order_by('data_hora')

    grafico_buffer_temperatura = gerar_grafico(
        localizacao, leituras_temperatura, 'Temperatura', 'r')
    grafico_buffer_umidade = gerar_grafico(
        localizacao, leituras_humidade, 'Umidade', 'g')
    grafico_buffer_ph = gerar_grafico(localizacao, leituras_ph, 'pH', 'b')

    context = {
        'localizacao': localizacao,
        'grafico_temperatura': grafico_buffer_temperatura,
        'grafico_umidade': grafico_buffer_umidade,
        'grafico_ph': grafico_buffer_ph,
    }

    return render(request, 'mostrarelatorio.html', context)


def gerar_grafico(localizacao, leituras, titulo, cor):
    fig, ax = plt.subplots(figsize=(8, 5))

    data = [leitura.data_hora for leitura in leituras]
    # Substitua 'valor' pelo campo correto
    valores = [leitura.valor for leitura in leituras]

    ax.plot(data, valores, label=titulo, color=cor)

    ax.set_xlabel('Data e Hora')
    ax.set_ylabel(titulo)
    ax.set_title(f'Leituras de {titulo} - {localizacao}')
    ax.legend()

    plt.tight_layout()

    canvas = FigureCanvas(fig)
    buffer = io.BytesIO()
    canvas.print_png(buffer)
    plt.close()

    buffer.seek(0)
    return buffer


def gerar_graficos(localizacao, leituras_temperatura: list[Leitura], leituras_humidade: list[Leitura], leituras_ph: list[Leitura]):
    fig, axs = plt.subplots(3, 1, figsize=(8, 15))

    data_temperatura = [leitura.data_hora for leitura in leituras_temperatura]
    temperatura = [leitura.valor for leitura in leituras_temperatura]

    data_humidade = [leitura.data_hora for leitura in leituras_humidade]
    humidade = [leitura.valor for leitura in leituras_humidade]

    data_ph = [leitura.data_hora for leitura in leituras_ph]
    ph = [leitura.valor for leitura in leituras_ph]

    axs[0].plot(data_temperatura, temperatura, label='Temperatura', color='r')
    axs[0].set_ylabel('Temperatura')
    axs[0].legend()

    axs[1].plot(data_humidade, humidade, label='Umidade', color='g')
    axs[1].set_ylabel('Umidade')
    axs[1].legend()

    axs[2].plot(data_ph, ph, label='pH', color='b')
    axs[2].set_xlabel('Data e Hora')
    axs[2].set_ylabel('pH')
    axs[2].legend()

    plt.tight_layout()

    canvas = FigureCanvas(fig)
    buffer = io.BytesIO()
    canvas.print_png(buffer)
    plt.close()

    buffer.seek(0)
    return buffer


# def gerar_grafico_temperatura(localizacao, leituras: list[Leitura]):
#     fig, ax = plt.subplots(figsize=(8, 5))

#     data = [leitura.data_hora for leitura in leituras]
#     temperatura = [leitura.valor for leitura in leituras]

#     ax.plot(data, temperatura, label='Temperatura', color='r')

#     ax.set_xlabel('Data e Hora')
#     ax.set_ylabel('Temperatura')
#     ax.set_title(f'Leituras de Temperatura - {localizacao}')
#     ax.legend()

#     plt.tight_layout()

#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     plt.close()

#     buffer.seek(0)
#     return buffer


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


def gerar_pdf(dados):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter)

    p.drawString(72, 800, "Relatório de Leituras")
    p.drawString(72, 780, datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"))

    y = 750
    for localizacao, media_temperatura, media_humidade, media_ph, leituras in dados:
        p.drawString(72, y, f"Localização: {localizacao}")
        p.drawString(72, y - 20, f"Média Temperatura: {media_temperatura}")
        p.drawString(72, y - 40, f"Média Umidade: {media_humidade}")
        p.drawString(72, y - 60, f"Média pH: {media_ph}")

        # Gerar gráficos de leituras históricas de temperatura, umidade e pH
        fig, ax = plt.subplots(figsize=(6, 4))

        data = [leitura.data_hora for leitura in leituras]
        temperatura = [leitura.temperatura for leitura in leituras]
        humidade = [leitura.humidade for leitura in leituras]
        ph = [leitura.ph for leitura in leituras]

        ax.plot(data, temperatura, label='Temperatura', color='r')
        ax.plot(data, humidade, label='Umidade', color='g')
        ax.plot(data, ph, label='pH', color='b')

        ax.set_xlabel('Data e Hora')
        ax.set_ylabel('Valor')
        ax.set_title('Leituras Históricas')
        ax.legend()

        plt.tight_layout()

        # Salvar o gráfico como uma imagem temporária
        temp_buffer = io.BytesIO()
        plt.savefig(temp_buffer, format='png')
        temp_buffer.seek(0)

        # Adicionar o gráfico ao PDF
        p.drawImage(temp_buffer, 72, y - 100, width=400, height=200)

        plt.close()

        y -= 320

    p.save()

    buffer.seek(0)
    return buffer
