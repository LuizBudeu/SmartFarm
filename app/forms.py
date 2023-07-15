from django import forms
from app.models import Dispositivo, Sensor, Leitura


class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = '__all__'


class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['modelo', 'tipo', 'ativo', 'valor_ideal']


class FiltroLocalizacaoForm(forms.Form):
    localizacoes = Dispositivo.objects.values_list(
        'localizacao', flat=True).distinct()
    LOCALIZACOES_CHOICES = [(localizacao, localizacao)
                            for localizacao in localizacoes]

    localizacao = forms.ChoiceField(
        choices=[('', 'Todas as Localizações')] + LOCALIZACOES_CHOICES, required=False)
