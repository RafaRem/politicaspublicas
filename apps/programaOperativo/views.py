from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.decorators import login_required
"""Forms"""
from apps.users.forms import RegistrarActividad
from apps.programaOperativo.forms import ProgramaOperativoForm, ActividadesForm
"""Modelos"""
from apps.programaOperativo.models import ProgramaOperativo
from apps.objetivo.models import Objetivo
from apps.objetivo.models import Objetivo
# Create your views here.
class ActividadFormView(View):
    def get(request):
        pass


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
            url = reverse('postPo',args=(idPo,))
            return redirect(url)

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
