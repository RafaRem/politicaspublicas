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

class ActividadFormView(View):
    """faltaría programa operativo, latitud, longitud, acciones en form"""
    def get(self,request):
        form = ActividadesForm()
        programasOperativos = ProgramaOperativo.objects.filter(
            dependencia=request.user.profile.dependencia.id
            )
        print(programasOperativos)
        return render(request,'programasOperativos/actividadForm.html',{
            'form':form,
            'programasOperativos':programasOperativos
        })
    def post(self,request):
        form = ActividadesForm(request.POST)
        if form.is_valid:
            datos = form.save(commit=False)
            accion = Acciones.objects.get(id=request.POST.get('accion'))
            datos.accion = accion
            po = ProgramaOperativo.objects.get(id=request.POST.get('programaoperativo'))
            datos.programaoperativo = po
            datos.user = request.user
            print(datos.user)
            print(datos.programaoperativo)
            print(datos.nombre)
            print(datos.descripcion)
            print(datos.presupuestoProgramado)
            print(datos.fecha_in)
            print(datos.fecha_fi)
            print(datos.accion)
            if datos.save():
                messages.success(request, 'Actividad registrada con éxito.')

        programasOperativos = ProgramaOperativo.objects.filter(
            dependencia=request.user.profile.dependencia.id
            )
        return render(request,'programasOperativos/actividadForm.html',{
            'form':form,
            'programasOperativos':programasOperativos
        })



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
