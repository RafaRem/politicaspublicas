from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.core import serializers
from django.contrib import messages
"""Models"""
from apps.programaOperativo.models import ProgramaOperativo
from apps.dependencia.models import Departamento
from apps.indicador.models import PeriodoGobierno


# Create your views here.
class ProgramasOperativosList(LoginRequiredMixin,View):
    """Will show all the department's operative programs"""
    login_url = 'login'
    def get_context(self,request):
        programasOperativos = ProgramaOperativo.objects.filter(estado='a',dependencia=request.user.profile.dependencia)
        programasOperativos = programasOperativos.order_by('nombre')
        departamentos = Departamento.objects.filter(dependencia=request.user.profile.dependencia)
        departamentos = departamentos.order_by('nombre')
        departamentos = serializers.serialize('json',departamentos)
        faltaPorAsignar = False
        for programaOperativo in programasOperativos:
            if not programaOperativo.departamento:
                faltaPorAsignar = True
                break
        return {
            'programasOperativos':programasOperativos,
            'departamentos':departamentos,
            'tieneDepartamentos':request.user.profile.dependencia.tieneDepartamentos,
            'faltaPorAsignar':faltaPorAsignar
        }
    def get(self,request):
        return render(request,'dependencias/programasoperativos.html',self.get_context(request))
    def post(self,request):
        #values comes separated by | where the first element is the operative program and the second is the department 
        valoresPo_Dep = request.POST.getlist('valoresDependencia')
        for valorPo_Dep in valoresPo_Dep:
            #0 value is the operative program's id and 1 is the department's id
            arrValor = valorPo_Dep.split('|')
            programaOperativo = ProgramaOperativo.objects.get(pk=arrValor[0])
            departamento = Departamento.objects.get(pk=arrValor[1])
            programaOperativo.departamento = departamento
            programaOperativo.save()
            pass
        messages.success(request,'Departamentos cambiados con éxito')
        return render(request,'dependencias/programasoperativos.html',self.get_context(request))        
    
class PresupuestoAnualList(LoginRequiredMixin,View):
    def obtenerContexto(self):
        periodos = PeriodoGobierno.objects.all()
        return {
            'periodos':periodos
        }
    def get(self,request,idProgramaOperativo):
        contexto = self.obtenerContexto()
        contexto['programaOperativo'] = ProgramaOperativo.objects.get(pk=idProgramaOperativo)
        return render(request,'dependencias/presupuestoAnual.html',contexto)
