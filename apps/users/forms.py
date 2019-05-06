#coding: utf-8
from django import forms
from .models import Persona
from django.core import validators

class RegistrarPersona(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'nombre', 
            'apellidopaterno',
            'apellidomaterno',
            'edad',
        ]
        labels = {
            'nombre': 'Nombre',
            'apellidopaterno':'Apellido Paterno',
            'apellidomaterno':'Apellido Materno',
            'edad': 'Edad',
        }
     