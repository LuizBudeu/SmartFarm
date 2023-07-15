from django import forms
from app.models import Dispositivo, Sensor, Leitura

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = '__all__'


class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor 
        fields = '__all__'
