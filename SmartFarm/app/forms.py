from django import forms
from app.models import Dispositivo

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = '__all__'
