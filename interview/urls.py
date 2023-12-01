#urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from my_app.views import index
from my_app.views import dashboard
from my_app.views import send_chart_data
from my_app.views import send_chart_data_humedad
from my_app.views import send_chart_data_predict
from my_app.views import send_chart_data_predict_humedad
from my_app.views import alarmas
from my_app.views import analitica
from my_app.views import send_temperatura_media_sensor1
from my_app.views import send_humedad_media_sensor1

# Author: Dario Fervenza
# Copyright: Copyright (c) [2023], Dario Fervenza
# Version: 0.1
# Maintainer: Dario Fervenza
# Email: dario.fervenza.garcia@gmail.com
# Status: Development

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name="login.html"),
        name='login'
        ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
        ),
    path("dashboard/", dashboard),
    path("send_chart_data/", send_chart_data),
    path("send_chart_data_humedad/", send_chart_data_humedad),
    path("send_chart_data_predict/",send_chart_data_predict),
    path(
        "send_chart_data_predict_humedad/",
        send_chart_data_predict_humedad
        ),
    path("alarmas/", alarmas),
    path("analitica",analitica),
    path(
        "send_temperatura_media_sensor1/",
        send_temperatura_media_sensor1
        ),
    path(
        "send_humedad_media_sensor1/",
        send_humedad_media_sensor1
        )
]
