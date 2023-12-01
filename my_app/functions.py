#functions.py
from typing import Tuple
import pandas as pd
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from sktime.forecasting.arima import ARIMA
from sktime.forecasting.theta import ThetaForecaster
from my_app.models import Temperaturas


# Author: Dario Fervenza
# Copyright: Copyright (c) [2023], Dario Fervenza
# Version: 0.1.0
# Maintainer: Dario Fervenza
# Email: dario.fervenza.garcia@gmail.com
# Status: Development

def obtener_ciudad (request, titulo: str) -> Tuple[int, str]:
    """ En la view donde se use esta funcion,
    esta funcion pedira el get,
    este get es enviado por el ajax,
    y esta funcion devuelve el titulo del grafico
    y la ciudad elegida en el get del ajax
    """
    opcion = request.GET.get('opcion')
    opcion = int(opcion)
    if opcion == 1:
        titulo += "Vigo"
    elif opcion == 2:
        titulo += "Lugo"
    elif opcion == 3:
        titulo += "Madrid"
    return opcion, titulo

def obtener_modelo (request) -> str:
    """Similar a obtener_ciudad pero solo
    devuleve el modelo pedido en el ajax
    """
    modelo = request.GET.get('modelo')
    modelo = str (modelo)
    return modelo

def extract_df_temperaturas():
    """ Funcion para obtener un df
    a partir de los objetos de
    la BBDD (instancias del modelo)
    """
    data_list = []
    data = Temperaturas.objects.all()
    for row in data:
        data_list.append({
            #al ser foreign key, no devulve el valor
            #sino el object del otro modelo OJO
            "sensor_id" : row.sensor_id.sensor_id,
            "fecha_medida" : row.fecha_medida,
            "temperatura" : row.temperatura,
            "humedad" : row.humedad
            })

    df = pd.DataFrame(data_list)
    df ["fecha_medida"] = pd.to_datetime(df ["fecha_medida"])
    df ["sensor_id"] = df ["sensor_id"].astype(int)
    return df

def create_ml_model(opcion, dato, redondeo, modelo):
    """funcion para crear el modelo de ML,
    crea el df a partir de extract_df_temperaturas
    y lo adapta para ser compatible con sktime.
    Divide el df para separar el df total
    y el df usado para predecir
    Una mejor solucion para detectar datos
    que se desvian de lo habitual quizas hubiese
    sido una tecnica de anomaly detection
    """
    if modelo == "exponential":
        forecaster = ExponentialSmoothing(
            trend='add',
            seasonal='add',
            sp=125
            )
    elif modelo == "arima":
        forecaster = ARIMA(order=(1, 1, 4))
    elif modelo == "theta":
        forecaster = ThetaForecaster(sp=55)
    df = extract_df_temperaturas()
    df.index = df ["fecha_medida"]
    df = df.loc[df["sensor_id"] == opcion]
    df.drop(
        ["fecha_medida", "sensor_id"],
        axis = 1,
        inplace = True
        )
    df = df[dato]
    df = df.resample("5T").mean()
    df.index = pd.PeriodIndex(df.index, freq="5T")
    df = df.fillna(method = "ffill")

    now = df.index.to_list()[-1]
    predict_time = df.index.to_list()[-75]
    now = pd.Period (now, freq="5T")
    predict_time = pd.Period (predict_time, freq="5T")
    # generamos los datos de tiempo (x)
    #para predecir sobre ellos (obtener y)
    period_range = pd.period_range(
        start = predict_time,
        end = now,
        freq = "5T"
        )
    df_entero = df.copy()
    df = df.loc[df.index <= predict_time]
    forecaster.fit(df)
    y_pred = forecaster.predict(period_range)
    y_pred = \
        y_pred.apply(lambda x : round(x, redondeo))
    return df, y_pred, df_entero
