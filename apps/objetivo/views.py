from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from apps.users.forms import RegistrarActividad
from apps.objetivo.models import Objetivo
"""Modelos"""
from apps.programaOperativo.models import ProgramaOperativo
# Create your views here.
class ObjetivosView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        acciones = []
        objetivos = []
        programasOperativos = ProgramaOperativo.objects.filter(dependencia=request.user.profile.dependencia)
        #itero todas las acciones de los programas y apilo su objetivo en una lista
        for programaOperativo in programasOperativos:
            accionesManyToMany = programaOperativo.acciones.all()
            for accion in accionesManyToMany:
                objetivos.append(accion.objetivo)
        #Quitas los objetivos repetidos
        objetivos = list(set(objetivos))
        return render(request,'objetivos/listObjetivos.html',{
            'objetivos':objetivos
        })