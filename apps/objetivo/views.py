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
        objetivos = Objetivo.objects.filter(dependencia=request.user.profile.dependencia)
        programasOperativos = ProgramaOperativo.objects.filter(dependencia=request.user.profile.dependencia)
        for objetivo in objetivos:
            x = ProgramaOperativo.objects.filter(objetivo=objetivo)
        return render(request,'objetivos/listObjetivos.html',{
            'objetivos':objetivos
        })