from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core import serializers
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
"""Forms"""
from apps.users.forms import RegistrarActividad
from apps.programaOperativo.forms import ProgramaOperativoForm, ActividadesForm
"""Modelos"""
from apps.programaOperativo.models import ProgramaOperativo, Acciones
from apps.objetivo.models import Objetivo
# # Create your views here.
# class ActividadFormView(View):
#     def get(request):
#         # form = ActividadesForm()
#         # return htt(request,'programasOperativos/actividadForm.html',{
#         #     'form':form
#         # })
#         return HttpResponse('hola mmundo')

def nueva_actividad_view(request):
    """faltaría programa operativo, latitud, longitud, acciones en form"""
    form = ActividadesForm()
    print(request.user.profile.dependencia)
    programasOperativos = ProgramaOperativo.objects.filter(
        dependencia=request.user.profile.dependencia.id
        )
    print(programasOperativos)
    return render(request,'programasOperativos/actividadForm.html',{
        'form':form,
        'programasOperativos':programasOperativos
    })

def get_acciones_po_view(request,idPo):
    programaOperativo = ProgramaOperativo.objects.get(id=idPo)
    acciones = serializers.serialize('json',programaOperativo.acciones.all())
    print(acciones)
    return JsonResponse(acciones,safe=False)
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
