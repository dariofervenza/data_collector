#models.py
from datetime import datetime
from django.db import models
from django.utils import timezone

fecha_actual = datetime.now()
fecha_actual = timezone.make_aware(fecha_actual)

# Author: Dario Fervenza
# Copyright: Copyright (c) [2023], Dario Fervenza
# Version: 0.1
# Maintainer: Dario Fervenza
# Email: dario.fervenza.garcia@gmail.com
# Status: Development

class SensoresDeTemperatura(models.Model):
    """id de sensor 1=Vigo 2=Lugo 3=Madrid
    """
    identificador = models.AutoField(
        primary_key = True
        )
    sensor_id = models.IntegerField(
        unique = True,
        null = False,
        blank = False
        )
    def __str__(self):
        return str(self.sensor_id)
class TipoDeAlarmas(models.Model):
    """limite superior, inferior o
    desviacion respecto a la prediccion
    """
    identificador = models.AutoField(
        primary_key = True
        )
    tipo_alarma = models.CharField(
        max_length = 75,
        null = False,
        blank = False,
        unique = True
        )
    def __str__(self):
        return str(self.tipo_alarma)
class TipoDeMedidas(models.Model):
    """ Temperatura o humedad
    """
    identificador = models.AutoField(
        primary_key = True
        )
    tipo_de_medida = models.CharField(
        max_length = 75,
        null = False,
        blank = False,
        unique = True
        )
    def __str__(self):
        return str(self.tipo_de_medida)
class Temperaturas(models.Model):
    """ Tabla que guarda los datos de
    los sensores que vienen de la api
    """
    identificador = models.AutoField(
        primary_key = True
        )
    sensor_id = models.ForeignKey(
        SensoresDeTemperatura,
        on_delete = models.CASCADE,
        to_field = "sensor_id"
        )
    fecha_medida = models.DateTimeField(
        auto_now_add=False,
        null=True,
        blank=True
        )
    temperatura = models.DecimalField(
        max_digits = 10,
        decimal_places = 5,
        null = False,
        blank = False
        )
    humedad = models.DecimalField(
        max_digits = 10,
        decimal_places = 5,
        null = False,
        blank = False
        )
class Alarmas(models.Model):
    """ Tabla que guarda las alarmas
    creadas
    """
    identificador = models.AutoField(
        primary_key = True
        )
    usuario = models.CharField(
        max_length = 50,
        null = False,
        blank = False
        )
    sensor_id = models.ForeignKey(
        SensoresDeTemperatura,
        on_delete = models.CASCADE,
        to_field = "sensor_id"
        )
    tipo_alarma = models.ForeignKey(
        TipoDeAlarmas,
        on_delete = models.CASCADE,
        to_field = "tipo_alarma"
        )
    tipo_de_medida = models.ForeignKey(
        TipoDeMedidas,
        on_delete = models.CASCADE,
        to_field = "tipo_de_medida",
        null = True
        )
    valor = models.DecimalField(
        max_digits = 10,
        decimal_places = 5,
        null = True,
        blank = False
        )
    fecha_creacion = models.DateTimeField(
        null=False,
        blank=False,
        default=fecha_actual
        )
    #AÑADIR CAMPO GRAVEDAD ALARMA
    #(LEVE, MODERADA, GRAVE)

class Avisos (models.Model):
    """ Tabla que guarda los avisos cuando
    salta una alarma
    """
    identificador = models.AutoField(
        primary_key = True
        )
    id_alarma = models.ForeignKey(
        Alarmas,
        on_delete = models.CASCADE,
        to_field = "identificador"
        )
    valor_sensor = models.DecimalField(
        max_digits = 10,
        decimal_places = 5,
        null = True,
        blank = False
        )
    fecha_sensor = models.DateTimeField(
        auto_now_add=False,
        null=True,
        blank=True
        )
    leido = models.BooleanField(
        default=False
        )
    usuario = models.CharField(
        max_length = 50,
        null = True,
        blank = False
        )
