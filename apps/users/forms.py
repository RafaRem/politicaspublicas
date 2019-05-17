#coding: utf-8
from django import forms
from .models import Persona, User
from apps.programaOperativo.models import Actividad
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

class UsuariosForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
     



class RegistrarActividad(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = [
            'user', 
            'programaoperativo',
            'nombre',
            'descripcion',
            'fecha_in',
            'fecha_fi',
        ]
        labels = {
            'user':'ID Usuario', 
            'programaoperativo':'ID Programa Operativo',
            'nombre':'Nombre',
            'descripcion':'Descripcion',
            'fecha_in':'Fecha Inicial',
            'fecha_fi':'Fecha Final',
        }