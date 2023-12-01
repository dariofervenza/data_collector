#views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import plotly.graph_objs as go
import plotly.io as pio
from my_app.models import Alarmas
from my_app.models import Avisos
from my_app.functions import extract_df_temperaturas
from my_app.functions import create_ml_model
from my_app.functions import obtener_ciudad
from my_app.functions import obtener_modelo
from my_app.forms import FormularioAlarmas
from my_app.tasks import generar_avisos

# Author: Dario Fervenza
# Copyright: Copyright (c) [2023], Dario Fervenza
# Version: 0.1.0
# Maintainer: Dario Fervenza
# Email: dario.fervenza.garcia@gmail.com
# Status: Development

pio.json.config.default_engine = 'orjson'

def index(request):
    return render(request, "index.html")

@login_required(login_url='/login/')
def dashboard(request):
    return render (request, "dashboard.html")

@login_required(login_url='/login/')
def alarmas(request):
    """ Crea la view de alarms,
    genera el formulario para crea nuevas
    alarmas y lo envia como contexto
    Ademas obtiene las alarmas ya creadas
    para el usuario actual y las muestra
    en la pagina
    """
    formulario_alarmas = FormularioAlarmas()
    usuario = request.user
    #obtener todas las alarmas
    #creadas para mostrarlas en la web
    alarmas_objects = \
        Alarmas.objects.filter(usuario = usuario)
    avisos = \
        Avisos.objects.filter(usuario = usuario)
    #obtener todos los avisos creados
    #para mostrarlas en la web
    if request.method == "POST":
        formulario_alarmas = \
            FormularioAlarmas(request.POST)
        if formulario_alarmas.is_valid():
            sensor_id = formulario_alarmas\
                        .cleaned_data["sensor_id"]
            tipo_alarma = formulario_alarmas\
                          .cleaned_data["tipo_alarma"]
            tipo_de_medida = formulario_alarmas\
                             .cleaned_data["tipo_de_medida"]
            valor = formulario_alarmas.cleaned_data["valor"]
            _, _ = Alarmas.objects.get_or_create(
                usuario = usuario,
                sensor_id = sensor_id,
                tipo_alarma = tipo_alarma,
                tipo_de_medida = tipo_de_medida,
                valor = valor
                ) # crear instancia de alarma
    generar_avisos()
    context = {
        "formulario_alarmas" : formulario_alarmas,
        "alarmas" : alarmas_objects,
        "avisos" : avisos
        } # enviar el formulario y
        #los datos de alarmas y avisos
    return render (
        request,
        "alarmas.html",
        context = context
        )
@login_required(login_url='/login/')
def analitica(request):
    """ Crea la view de analytics
    """
    return render (request, "analitica.html")
@login_required(login_url='/login/')
def send_chart_data(request):
    """ Funcion para crear el grafico de
    datos de temperaturas segun la
    ciudad se descarga con js y ajax,
    el ajax pide el get de esta
    view con parametros y luego
    crea el plot con js +plotly
    """
    titulo = "Temperatura en "
    opcion, titulo = obtener_ciudad (request, titulo)
    df = extract_df_temperaturas()
    df = df.loc[df["sensor_id"] == opcion]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = df["fecha_medida"],
            y = df["temperatura"]
            )
        )
    fig.update_layout(
        title = titulo,
        xaxis_title = "Fecha",
        yaxis_title = "Temperatura"
        )
    fig_json = pio.to_json(fig)
    return JsonResponse(
        {'figure': fig_json}
        )
@login_required(login_url='/login/')
def send_chart_data_humedad(request):
    """ Funcion para crear el
    grafico de datos de humedades
    segun la ciudad
    Lo envia como respuesta para
    renderizarlo con pltly.js en
    la template
    """
    titulo = "Humedad en "
    opcion, titulo = \
        obtener_ciudad (request, titulo)
    df = extract_df_temperaturas()
    df = df.loc[df["sensor_id"] == opcion]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = df["fecha_medida"],
            y = df["humedad"]
            )
        )
    fig.update_layout(
        title = titulo,
        xaxis_title = "Fecha",
        yaxis_title = "Humedad"
        )
    fig_json = pio.to_json(fig)
    return JsonResponse(
        {'figure': fig_json}
        )
@login_required(login_url='/login/')
def send_chart_data_predict(request):
    """ Funcion para crear el grafico
    de datos de temperaturas + la
    prediccion de ellas segun la ciudad
    """
    titulo = "Predicción temperatura en "
    opcion, titulo = \
        obtener_ciudad (request, titulo)
    modelo = obtener_modelo (request)
    _, y_pred, df_entero = create_ml_model(
        opcion = opcion,
        dato = "temperatura",
        redondeo = 3,
        modelo = modelo
        )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = df_entero.index.to_timestamp(),
            y = df_entero.iloc[:],
            name = "Original"
            )
        )
    fig.add_trace(
        go.Scatter(
            x = y_pred.index.to_timestamp(),
            y = y_pred.iloc[:],
            name = "Predicción"
            )
        )
    fig.update_layout(
        title = titulo,
        xaxis_title = "Fecha",
        yaxis_title = "Temperatura"
        )
    fig_json = pio.to_json(fig)
    return JsonResponse(
        {'figure': fig_json}
        )
@login_required(login_url='/login/')
def send_chart_data_predict_humedad(request):
    """ Funcion para crear el grafico de
    datos de humedades + la prediccion
    de ellas  segun la ciudad
    """
    titulo = "Predicción humedad en "
    opcion, titulo = \
        obtener_ciudad (request, titulo)
    modelo = obtener_modelo (request)
    _, y_pred, df_entero = \
        create_ml_model(
            opcion = opcion,
            dato = "humedad",
            redondeo = 3,
            modelo = modelo
            )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = df_entero.index.to_timestamp(),
            y = df_entero.iloc[:],
            name = "Original"
            )
        )
    fig.add_trace(
        go.Scatter(
            x = y_pred.index.to_timestamp(),
            y = y_pred.iloc[:],
            name = "Predicción"
            )
        )
    fig.update_layout(
        title = titulo,
        xaxis_title = "Fecha",
        yaxis_title = "Humedad"
        )
    fig_json = pio.to_json(fig)
    return JsonResponse(
        {'figure': fig_json}
        )
@login_required(login_url='/login/')
def send_temperatura_media_sensor1(request):
    """ Funcion para crear el grafico
    de temperatura media, se aplica
    a cada ciudad
    """
    titulo = "Temperatura media en "
    opcion, titulo = \
        obtener_ciudad (request, titulo)
    df = extract_df_temperaturas()
    df = df.groupby("sensor_id")["temperatura"].mean()
    df = df.loc[df.index == opcion]
    valor = df.iloc[0]
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = valor,
        title={'text': titulo},
        domain={'x': [0, 1], 'y': [0, 1]},
        ))
    fig.update_layout(
        margin={"l" : 20, "r" : 20, "t" : 20, "b" : 20},
        width =  350
        )
    fig_json = pio.to_json(fig)
    return JsonResponse(
        {"figure" : fig_json}
        )
@login_required(login_url='/login/')
def send_humedad_media_sensor1(request):
    """ Funcion para crear el grafico
    de humedad media, se aplica a cada ciudad
    """
    titulo = "Humedad media en "
    opcion, titulo = obtener_ciudad (request, titulo)
    df = extract_df_temperaturas()
    df = df.groupby("sensor_id")["humedad"].mean()
    df = df.loc[df.index == opcion]
    valor = df.iloc[0]
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = valor,
        title={'text': titulo},
        domain={'x': [0, 1], 'y': [0, 1]},
        ))
    fig.update_layout(
        margin={"l" : 20, "r" : 20, "t" : 20, "b" : 20},
        width =  350
    )
    fig_json = pio.to_json(fig)
    return JsonResponse(
        {"figure" : fig_json}
        )
