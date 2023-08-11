from django.db import models


class Dispositivo(models.Model):

    modelo = models.CharField(max_length=100, blank=True, null=True)
    localizacao = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dispositivo'


class Sensor(models.Model):

    modelo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    ultima_leitura = models.DateTimeField(blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    valor_ideal = models.FloatField(blank=True, null=True)
    dispositivo = models.ForeignKey(
        Dispositivo, on_delete=models.CASCADE, related_name='sensores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sensor'


class Leitura(models.Model):

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    valor = models.FloatField(blank=True, null=True)
    unidade_medida = models.CharField(max_length=100, blank=True, null=True)
    data_hora = models.DateTimeField()

    class Meta:
        db_table = 'leitura'
