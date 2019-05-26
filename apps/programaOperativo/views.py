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
from apps.programaOperativo.models import ProgramaOperativo, Acciones, Actividad
from apps.objetivo.models import Objetivo
# # Create your views here.
def get_acciones_po_view(request,idPo):
    programaOperativo = ProgramaOperativo.objects.get(id=idPo)
    acciones = serializers.serialize('json',programaOperativo.acciones.all())
    print(acciones)
    return JsonResponse(acciones,safe=False)
    pass

class ActividadesListView(View):
    def get(self,request):
        pos = ProgramaOperativo.objects.filter(dependencia=request.user.profile.dependencia)
        actividades = []
        for po in pos:
            actividadesPo = Actividad.objects.filter(programaoperativo=po)
            for actividadPo in actividadesPo:
                actividades.append(actividadPo)
                pass
            pass
        print(actividades)
        return render(request,'programasOperativos/actividades/listActividades.html',{
            'actividades':actividades
        })

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
    def get(self,request):
        form = ActividadesForm()
        programasOperativos = ProgramaOperativo.objects.filter(
            dependencia=request.user.profile.dependencia.id
            )
        print(programasOperativos)
        return render(request,'programasOperativos/actividades/actividadForm.html',{
            'form':form,
            'programasOperativos':programasOperativos
        })
    def post(self,request):
        form = ActividadesForm(request.POST)
        if form.is_valid():
            datos = form.save(commit=False)
            accion = Acciones.objects.get(id=request.POST.get('accion'))
            datos.accion = accion
            po = ProgramaOperativo.objects.get(id=request.POST.get('programaoperativo'))
            datos.programaoperativo = po
            datos.user = request.user
            datos.latitud = request.POST.get('latitud')
            datos.longitud = request.POST.get('longitud')
            save = datos.save()
            messages.success(request, 'Actividad registrada con éxito.')
            return redirect('listActividades')
        messages.error('Error al cargar, intente de nuevo.')
        programasOperativos = ProgramaOperativo.objects.filter(
            dependencia=request.user.profile.dependencia.id
            )
        return render(request,'programasOperativos/actividades/actividadForm.html',{
            'form':form,
            'programasOperativos':programasOperativos
        })

class TerminarActividadFormView(View):
    def get(self,request,idActividad):
        """validar si ya subió información no pueda acceder"""
        actividad = Actividad.objects.get(pk=idActividad)
        form = ActividadesForm()
        return render(request,'programasOperativos/actividades/terminarActividad.html',{
            'form':form,
            'actividad':actividad
        })
    def post(self,request,idActividad):
        form = ActividadesForm(request.POST)
        if form.is_valid():
            datos = form.save(commit=False)
            accion = Acciones.objects.get(id=request.POST.get('accion'))
            datos.accion = accion
            po = ProgramaOperativo.objects.get(id=request.POST.get('programaoperativo'))
            datos.programaoperativo = po
            datos.user = request.user
            datos.latitud = request.POST.get('latitud')
            datos.longitud = request.POST.get('longitud')
            save = datos.save()
            messages.success(request, 'Actividad registrada con éxito.')
            return redirect('terminarActividad')
        messages.error('Error al cargar, intente de nuevo.')
        programasOperativos = ProgramaOperativo.objects.filter(
            dependencia=request.user.profile.dependencia.id
            )
        return render(request,'programasOperativos/actividades/actividadForm.html',{
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
