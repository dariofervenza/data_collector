#tasks.py
import time
from datetime import datetime
import requests
from celery import shared_task
from django.utils import timezone
from django.db.models import Q
from my_app.models import Temperaturas
from my_app.models import SensoresDeTemperatura
from my_app.models import Avisos
from my_app.models import Alarmas

# Author: Dario Fervenza
# Copyright: Copyright (c) [2023], Dario Fervenza
# Version: 0.1
# Maintainer: Dario Fervenza
# Email: dario.fervenza.garcia@gmail.com
# Status: Development

@shared_task
def obtener_dato(ciudad):
    """ Obtener datos de T, humedad
    y fecha medida de la API
    """
    date_format = "%Y-%m-%d %H:%M"
    params = {
        'access_key': 'super_secret_key',
        'query': ciudad
    }
    api_result = requests.get(
        'http://api.weatherstack.com/current',
        params
        )
    api_response = api_result.json()
    fecha_actual = \
        api_response ["location"]["localtime"]
    fecha_actual = datetime.strptime(
        fecha_actual,
        date_format
        )
    fecha_actual = \
        timezone.make_aware(fecha_actual)
    temperatura = \
        api_response ["current"]["temperature"]
    humedad = \
        api_response ["current"]["humidity"]
    return fecha_actual, temperatura, humedad

@shared_task
def guardar_temperaturas():
    """ Guardar los datos de T,
    humedad y fecha medida en la BBDD
    para gran cantidad de
    sensor_id y ciudades usar
    for sensor, id in
    zip(lista_sensor, lista_ciudades)
    """
    fecha_actual, temperatura, humedad = \
        obtener_dato(ciudad = "Vigo")
    sensor_id = 1
    sensor_obj = \
        SensoresDeTemperatura.objects.get(
            sensor_id = sensor_id
            )
    #- USAR MEJOR GET_OR_CREATE
    #LA API A VECES ENVIA EL MISMO
    #VALOR Y SALEN DUPLICAODS
    Temperaturas(
        sensor_id = sensor_obj,
        fecha_medida = fecha_actual,
        temperatura = temperatura,
        humedad = humedad
        ).save()
    time.sleep(0.5)
    fecha_actual, temperatura, humedad = \
        obtener_dato(ciudad = "Lugo")
    sensor_id = 2
    sensor_obj = \
        SensoresDeTemperatura.objects.get(
            sensor_id = sensor_id
            )
    Temperaturas(
        sensor_id = sensor_obj,
        fecha_medida = fecha_actual,
        temperatura = temperatura,
        humedad = humedad
        ).save()
    time.sleep(0.5)
    fecha_actual, temperatura, humedad = \
        obtener_dato(ciudad = "Madrid")
    sensor_id = 3
    sensor_obj = \
        SensoresDeTemperatura.objects.get(
            sensor_id = sensor_id
            )
    Temperaturas(
        sensor_id = sensor_obj,
        fecha_medida = fecha_actual,
        temperatura = temperatura,
        humedad = humedad
        ).save()
    time.sleep(0.5)
@shared_task
def generar_avisos():
    """ Calcular y guardar los avisos
    de alarmas en la BBDD # deberia
    ser un daemon con celery, pero
    se ejecuta al ver la view
    de alarmas de momento ¿?
    """
    mis_alarmas = Alarmas.objects.all()
    for alarma in mis_alarmas:
        sensor_id = alarma.sensor_id.sensor_id
        tipo_alarma = \
            alarma.tipo_alarma.tipo_alarma
        tipo_de_medida = \
            alarma.tipo_de_medida.tipo_de_medida
        valor = alarma.valor
        identificador = alarma.identificador
        identificador = \
            Alarmas.objects.get(identificador = identificador)
        mis_datos = Temperaturas.objects.filter(Q(
            sensor_id = sensor_id
            ))
        usuario = alarma.usuario
        #SE PODRIA AÑADIR QUE SI DETECTA
        #UNA ALARMA, SE SALTE TRES BUCLES,
        # ES DECIR, QUE ESTÉ 30 MINUTOS SIN
        #GENERAR OTRA PARA NO SOBRECARGAR
        if tipo_de_medida == "Temperatura":
            for dato in mis_datos:
                if dato.temperatura > valor \
                and tipo_alarma == "Limite superior":
                    _, _ = Avisos.objects.get_or_create(
                        id_alarma = identificador,
                        valor_sensor = dato.temperatura,
                        fecha_sensor = dato.fecha_medida,
                        usuario = usuario
                        )
        elif tipo_de_medida == "Humedad":
            for dato in mis_datos:
                if dato.humedad > valor \
                and tipo_alarma == "Limite superior":
                    _, _ = Avisos.objects.get_or_create(
                        id_alarma = identificador,
                        valor_sensor = dato.humedad,
                        fecha_sensor = dato.fecha_medida,
                        usuario = usuario)
