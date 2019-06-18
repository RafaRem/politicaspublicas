from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
"""Forms"""
from apps.users.forms import RegistrarActividad
from apps.programaOperativo.forms import ProgramaOperativoForm, ActividadesForm, TerminarActividadesForm
"""Modelos"""
from apps.programaOperativo.models import ProgramaOperativo, Acciones, Actividad, DetallesGasto
from apps.objetivo.models import Objetivo
from apps.indicador.models import ConceptoGasto, ClasificacionGasto
# # Crea
# te your views here.
#ESTE NO NECESITA PROTECCION
def get_acciones_po_view(request,idPo):
    programaOperativo = ProgramaOperativo.objects.get(id=idPo)
    acciones = serializers.serialize('json',programaOperativo.acciones.all())
    return JsonResponse(acciones,safe=False)
    pass

class ActividadesListView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        pos = ProgramaOperativo.objects.filter(dependencia=request.user.profile.dependencia)
        actividades = []
        for po in pos:
            actividadesPo = Actividad.objects.filter(programaoperativo=po)
            for actividadPo in actividadesPo:
                actividades.append(actividadPo)
                pass
            pass
        return render(request,'programasOperativos/actividades/listActividades.html',{
            'actividades':actividades
        })

class ProgramasOperativosView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request, idPo):
        programa = ProgramaOperativo.objects.get(id=idPo)
        form = ProgramaOperativoForm(instance=programa)
        return render(request, 'programasOperativos/poForm.html',{
            'form':form,
            'acciones': programa.acciones.all()
        })
    def post(self,request, idPo):
        programa = ProgramaOperativo.objects.get(id=idPo)
        form = ProgramaOperativoForm(request.POST,instance=programa)
        if form.is_valid():
            form.save()
            messages.success(request,'Actualizado con éxito')
            url = reverse('postPo',args=(idPo,))
            return redirect(url)

class ActividadFormView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        form = ActividadesForm()
        programasOperativos = ProgramaOperativo.objects.filter(
            dependencia=request.user.profile.dependencia.id
            )
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
            datos.fecha_in = request.POST.get('fecha_in')
            datos.fecha_fi = request.POST.get('fecha_fi')
            save = datos.save()
            actividad = Actividad.objects.latest('created')
            idActividad = actividad.id
            messages.success(request, 'Actividad registrada con éxito.')
            url = reverse('terminarActividad',args=(idActividad,))
            return redirect(url)
            # return redirect('terminarActividad',args)

        messages.error(request,form._errors)
        programasOperativos = ProgramaOperativo.objects.filter(
            dependencia=request.user.profile.dependencia.id
            )
        return render(request,'programasOperativos/actividades/actividadForm.html',{
            'form':form,
            'programasOperativos':programasOperativos
        })

class TerminarActividadFormView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,idActividad):
        """validar si ya subió información no pueda acceder"""
        actividad = Actividad.objects.get(pk=idActividad)
        form = TerminarActividadesForm()
        if request.user.profile.dependencia.tipo == 'd':
            conceptosGasto = ConceptoGasto.objects.filter(tipoDependencia='d')
        else:
            conceptosGasto = ConceptoGasto.objects.filter(tipoDependencia='p',dependencia=request.user.profile.dependencia)
        conceptosGasto = serializers.serialize('json',conceptosGasto, use_natural_foreign_keys=True)
        return render(request,'programasOperativos/actividades/terminarActividad.html',{
            'form':form,
            'actividad':actividad,
            'conceptosGasto':conceptosGasto
        })
    def post(self,request,idActividad):
        actividad = Actividad.objects.get(pk=idActividad)
        form = TerminarActividadesForm(request.POST, instance=actividad)
        if form.is_valid():
            datos = form.save(commit=False)
            archivo = request.FILES['archivos']
            datos.evidencia = archivo
            #'t' significa terminada
            datos.estado = 't'
            gastosActividad = request.POST.getlist('gastos[]')
            for gasto in gastosActividad:
                gasto = gasto.split('|')
                conceptoGasto = ConceptoGasto.objects.get(pk=gasto[1])
                DetallesGasto.objects.create(
                    cantidad=gasto[0],
                    actividad=actividad,
                    gasto=conceptoGasto
                )
            save = datos.save()
            messages.success(request, 'Actividad actualizada con éxito.')
            return redirect('listActividades')
        messages.error(request, form._errors)
        #Si hay algún error inesperado recarga la página
        actividad = Actividad.objects.get(pk=idActividad)
        form = TerminarActividadesForm()
        conceptosGasto = ConceptoGasto.objects.all()
        conceptosGasto = serializers.serialize('json',conceptosGasto, use_natural_foreign_keys=True)
        return render(request,'programasOperativos/actividades/terminarActividad.html',{
            'form':form,
            'actividad':actividad,
            'conceptosGasto':conceptosGasto
        })

class ProgramasOperativosListView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idObjetivo = 0):
        #SI EL OBJETIVO DE LA ACCION PERTENECE A ESTE ID, SE ALMACENARÁ ACÁ
        programasOperativos = []
        objetivo = Objetivo.objects.get(id=idObjetivo)
        if idObjetivo != 0:
            programas = ProgramaOperativo.objects.filter(
                dependencia=request.user.profile.dependencia
            )
            for programa in programas:
                acciones = programa.acciones.all()
                for accion in acciones:
                    if idObjetivo == accion.objetivo.id:
                        programasOperativos.append(programa)
            programasOperativos = list(set(programasOperativos))
            return render(request,'programasOperativos/listPoObjetivo.html',{
            'programas':programasOperativos,
            'objetivo':objetivo
            })

        programas = ProgramaOperativo.objects.all()
        return render(request,'programasOperativos/listPoObjetivo.html',{
            'programas':programas,
            'objetivo':objetivo
        })

def ver_actividad(request,idActividad):
    actividad = Actividad.objects.get(pk=idActividad)
    return render(request,'programasOperativos/actividades/verActividad.html',{
        'actividad':actividad
    })