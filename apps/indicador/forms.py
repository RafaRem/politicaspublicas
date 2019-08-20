from django import forms
from apps.indicador.models import Configuracion

class ConfiguracionesForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = '__all__'
