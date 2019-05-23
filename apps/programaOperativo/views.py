from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from apps.users.forms import RegistrarActividad
from apps.objetivo.models import Objetivo
from apps.programaOperativo.forms import ProgramaOperativoForm
"""Modelos"""
from apps.programaOperativo.models import ProgramaOperativo
from apps.objetivo.models import Objetivo
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
    def get(self, request, idPo):
        programa = ProgramaOperativo.objects.get(id=idPo)
        form = ProgramaOperativoForm(instance=programa)
        return render(request, 'programasOperativos/poForm.html',{
            'form':form
        })
    def post(self,request, idPo):
        programa = ProgramaOperativo.objects.get(id=idPo)
        form = ProgramaOperativoForm(request.POST,instance=programa)
        if form.is_valid():
            form.save()
            messages.success(request,'Actualizado con éxito')
            redirect('updateProgramaOperativo')

class ProgramasOperativosListView(View):
    def get(self,request, idObjetivo = 0):
        objetivo = Objetivo.objects.get(id=idObjetivo)
        if idObjetivo != 0:
            programas = ProgramaOperativo.objects.filter(
                dependencia=request.user.profile.dependencia,
                objetivo=idObjetivo
            )
            return render(request,'programasOperativos/listPoObjetivo.html',{
            'programas':programas,
            'objetivo':objetivo
            })

        programas = ProgramaOperativo.objects.all()
        return render(request,'programasOperativos/listPoObjetivo.html',{
            'programas':programas,
            'objetivo':objetivo
        })
