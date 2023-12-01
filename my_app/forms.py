#forms.py

from django import forms
from my_app.models import Alarmas

# Author: Dario Fervenza
# Copyright: Copyright (c) [2023], Dario Fervenza
# Version: 0.1.0
# Maintainer: Dario Fervenza
# Email: dario.fervenza.garcia@gmail.com
# Status: Development

class FormularioAlarmas(forms.ModelForm):
    """formulario para crear alarmas,
    no hay necesidad de querset por pocas
    datos, valorarlo si hay muchos sensores
    """
    class Meta:
        model = Alarmas
        fields = [
            "sensor_id", "tipo_alarma",
            "tipo_de_medida", "valor"
            ]
