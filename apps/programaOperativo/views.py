from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from apps.users.forms import RegistrarActividad
from apps.objetivo.models import Objetivo
"""Modelos"""
from apps.programaOperativo.models import ProgramaOperativo
# Create your views here.
def Actividad(request):
    if request.method=='POST':
        form = RegistrarActividad(request.POST)
        if form.is_valid():
                messages.success(request,"Registro con exito")
                form.save()
        return redirect("Regactividad")
    else:
        form = RegistrarActividad()
    return render(request,'users/RegistroActividad.html',{})

class ProgramasOperativosView(View):
    def get(self, request):
        objetivos = Objetivo.objects.filter(dependencia=request.user.profile.dependencia)
        programasOperativos = ProgramaOperativo.objects.filter(dependencia=request.user.profile.dependencia)
        for objetivo in objetivos:
            x = ProgramaOperativo.objects.filter(objetivo=objetivo)
        return render(request,'programasOperativos/list.html',{
            'objetivos':objetivos
        })

