from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.core import serializers
"""Models"""
from apps.programaOperativo.models import ProgramaOperativo
from apps.dependencia.models import Departamento


# Create your views here.
class ProgramasOperativosList(LoginRequiredMixin,View):
    """Will show all the department's operative programs"""
    login_url = 'login'
    def get(self,request):
        programasOperativos = ProgramaOperativo.objects.filter(estado='a',dependencia=request.user.profile.dependencia)
        programasOperativos = programasOperativos.order_by('nombre')
        departamentos = Departamento.objects.filter(dependencia=request.user.profile.dependencia)
        departamentos = departamentos.order_by('nombre')
        departamentos = serializers.serialize('json',departamentos)
        return render(request,'dependencias/programasoperativos.html',{
            'programasOperativos':programasOperativos,
            'departamentos':departamentos
        })

