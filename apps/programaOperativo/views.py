import json
import datetime
import os
import threading
import queue
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
"""Forms"""
from apps.users.forms import RegistrarActividad
from apps.programaOperativo.forms import ProgramaOperativoForm, ActividadesForm, TerminarActividadesForm, RevalidarActividadesForm
"""Modelos"""
from apps.programaOperativo.models import ProgramaOperativo, Acciones, Actividad, DetallesGasto, LogActividad
from apps.objetivo.models import Objetivo
from apps.indicador.models import ConceptoGasto, ClasificacionGasto,Periodo,PeriodoGobierno
from apps.dependencia.models import Dependencia
from django.db.models import Q,Count
"""Serializer"""
from apps.programaOperativo.serializers import AccionesSerializer
from rest_framework.renderers import JSONRenderer

def filtroProgramasOperativos(id_objetivo=0,id_dependencia=0):
    consulta = Q(estado='a')
    programasOperativos = []
    if id_dependencia > 0:
        dependencia = Dependencia.objects.get(pk=id_dependencia)
        consulta &= Q(dependencia=id_dependencia)
    #Hacemos la consulta, se deja al final el filtro por objetivo por complejidad
    programas = ProgramaOperativo.objects.filter(consulta)    
    if id_objetivo > 0:
        programasOperativos = []
        for programa in programas:
            acciones = programa.acciones.all()
            for accion in acciones:
                if id_objetivo == accion.objetivo.id:
                    programasOperativos.append(programa)
        programasOperativos = list(set(programasOperativos))
        return programasOperativos
    return programas

def filtroAcciones(id_dependencia=0,id_objetivo=0,id_eje="",id_programaOperativo=0):
    #TO-DO: 
    #FALTA TERMINAR
    consulta = Q()
    if id_objetivo>0:
        objetivo = Objetivo.objects.get(pk=id_objetivo)
        consulta &= Q(objetivo=objetivo)
    if id_eje!="":
        consulta&=Q(objetivo__ejeTransversal=id_eje)
    acciones =  Acciones.objects.filter(consulta)
    #hasta aquí comenzamos a hacerlo casi manual        

def filtroActividades(id_dependencia=0,estado="",id_objetivo=0,id_eje="",id_programaOperativo=0):
    #No se aplicará filtros si los parametros son iguales 0 o ""
    consulta = Q()
    if id_dependencia>0:
        dependencia = Dependencia.objects.get(pk=id_dependencia)
        consulta &= Q(programaoperativo__dependencia=dependencia)
    if estado!="":
        consulta &= Q(estado=estado)
    if id_objetivo>0:
        objetivo = Objetivo.objects.get(pk=id_objetivo)
        consulta &= Q(accion__objetivo=objetivo)
    if id_eje!="":
        consulta&=Q(accion__objetivo__ejeTransversal=id_eje)
    if id_programaOperativo>0:
        po = ProgramaOperativo.objects.get(pk=id_programaOperativo)
        consulta &= Q(programaoperativo=po)
    actividades = Actividad.objects.filter(consulta)        
    return actividades

def corregirAcciones(request):
    """Script to correct actions from the database, it gets just the number"""
    acciones = Acciones.objects.all()
    for accion in acciones:
        cadena =  accion.meta
        if cadena:
            entero = [int(s) for s in cadena.split() if s.isdigit()]
            if entero:
                descripcionMeta = str(accion.descripcionMeta)
                meta = str(entero[0]) + ' ' + descripcionMeta
                if accion.descripcionMeta:
                    accion.descripcionMeta = accion.meta + ' ' + descripcionMeta
                else:
                    accion.descripcionMeta = accion.meta
                accion.meta = str(entero[0]) 
                accion.save()
            else:
                accion.meta = ""
                # accion.save()
    return HttpResponse('listón')
            
def filtroDependencias(id_objetivo=0):
    dependencias = []
    if id_objetivo > 0:
        programasOperativos = filtroProgramasOperativos(id_objetivo=id_objetivo)
        for po in programasOperativos:
            dependencias.append(po.dependencia)
        dependencias = list(set(dependencias))        
    return dependencias

def filtroObjetivos(id_eje="", tipo=""):
    consulta = Q(estado='a')
    if id_eje!="":
        consulta &= Q(ejeTransversal=id_eje)
    if tipo!="":
        consulta &= Q(tipo=tipo)
    objetivos = Objetivo.objects.filter(consulta)
    return objetivos

#ESTE NO NECESITA PROTECCION
def get_acciones_po_view(request,idPo):
    programaOperativo = ProgramaOperativo.objects.get(id=idPo)
    acciones = serializers.serialize('json',programaOperativo.acciones.all())
    return JsonResponse(acciones,safe=False)
    pass

#todas las vistas que tienen que ver con programas operativos no admin
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

class ProgramasOperativosListView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idObjetivo = 0):
        #SI EL OBJETIVO DE LA ACCION PERTENECE A ESTE ID, SE ALMACENARÁ ACÁ
        programasOperativos = []
        objetivo = Objetivo.objects.get(id=idObjetivo)
        if idObjetivo != 0:
            programasOperativos = filtroProgramasOperativos(
                id_dependencia=request.user.profile.dependencia.id,
                id_objetivo=idObjetivo
                )

            return render(request,'programasOperativos/listPoObjetivo.html',{
            'programas':programasOperativos,
            'objetivo':objetivo
            })

        programas = ProgramaOperativo.objects.all()
        return render(request,'programasOperativos/listPoObjetivo.html',{
            'programas':programas,
            'objetivo':objetivo
        })

@login_required(login_url='login')
def ver_actividad(request,idActividad):
    actividad = Actividad.objects.get(pk=idActividad)
    return render(request,'programasOperativos/actividades/verActividad.html',{
        'actividad':actividad
    })

@login_required(login_url='login')
def ver_accion(request,idAccion):
    accion = Acciones.objects.get(pk=idAccion)
    detallesGasto = DetallesGasto.objects.filter(accion=accion)
    periodos = Periodo.objects.all()
    return render(request,'programasOperativos/accion.html',{
        'accion':accion,
        'detallesGasto':detallesGasto,
        'periodos': periodos
    })

#Todas las vistas que tienen que ver con actividades no de administrador
class CapturarGastoView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,idAccion,idPeriodo):
        accion = Acciones.objects.get(pk=idAccion)
        periodo = Periodo.objects.get(pk=idPeriodo)
        if periodo.capturaHabilitada == False:
            messages.error(request,'La captura de este periodo está inhabilitada')
            url = reverse('verAccion',args=(idAccion,))
            return redirect(url)
        #Si es dependencia o paramunicipal cargará otros conceptos de gasto
        if request.user.profile.dependencia.tipo == 'd':
            conceptosGasto = ConceptoGasto.objects.filter(tipoDependencia='d')
        else:
            conceptosGasto = ConceptoGasto.objects.filter(tipoDependencia='p',dependencia=request.user.profile.dependencia)
        detallesGasto = DetallesGasto.objects.filter(accion=accion,periodo=periodo)
        conceptosGasto = serializers.serialize('json',conceptosGasto, use_natural_foreign_keys=True)
        return render(request,'programasOperativos/capturarGastos.html',{
            'conceptosGasto':conceptosGasto
        })
    def post(self, request, idAccion, idPeriodo):
        accion = Acciones.objects.get(pk=idAccion)
        periodo = Periodo.objects.get(pk=idPeriodo)
        gastosAccion = request.POST.getlist('gastos[]')
        detallesGasto = DetallesGasto.objects.filter(accion=accion,periodo=periodo)
        detallesGasto.delete()
        for gasto in gastosAccion:
            gasto = gasto.split('|')
            conceptoGasto = ConceptoGasto.objects.get(pk=gasto[1])
            objeto = DetallesGasto.objects.create(
                cantidad=gasto[0],
                accion=accion,
                periodo=periodo,
                gasto=conceptoGasto
            )
            objeto.save()
        messages.success(request,'Se han capturado los gastos exitosamente')
        url = reverse('verAccion',args=(idAccion,))
        return redirect(url)
    
@login_required(login_url='login')
def ver_gastos(request,idAccion,idPeriodo):
    accion = Acciones.objects.get(pk=idAccion)
    periodo =  Periodo.objects.get(pk=idPeriodo)
    gastos = DetallesGasto.objects.filter(accion=accion,periodo=periodo)
    total = 0
    for gasto in gastos:
        total += float(gasto.cantidad)
    return render(request,'programasOperativos/verGastos.html',{
        'gastos':gastos,
        'total':total
    })

class EditarGastosView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,idAccion,idPeriodo):
        accion = Acciones.objects.get(pk=idAccion)
        periodo = Periodo.objects.get(pk=idPeriodo)
        if periodo.capturaHabilitada == False:
            messages.error(request,'La captura de este periodo está inhabilitada')
            url = reverse('verAccion',args=(idAccion,))
            return redirect(url)
        gastos = DetallesGasto.objects.filter(accion=accion,periodo=periodo)
        return render(request,'programasOperativos/editarGastos.html',{
            'gastos':gastos
        })
    def post(self,request,idAccion,idPeriodo):
        accion = Acciones.objects.get(pk=idAccion)
        periodo = Periodo.objects.get(pk=idPeriodo)
        gastos = request.POST.getlist('gastos[]')
        for gasto in gastos:
            gasto = gasto.split('|')
            objeto =  DetallesGasto.objects.get(pk=gasto[1])
            objeto.cantidad = gasto[0]
            objeto.save()
            pass
        messages.success(request,'Se han actualizado los datos exitosamente')
        url = reverse('verAccion',args=(idAccion,))
        return redirect(url)

class ReporteActividadesEnlaceView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        #En este arreglo se guardará lo que se mostrará en gráfica
        arreglo = []
        actividades = Actividad.objects.filter(programaoperativo__dependencia=request.user.profile.dependencia,
        estado='p')
        arreglo.append({'name':'Programadas','y':actividades.count()})
        actividades = Actividad.objects.filter(programaoperativo__dependencia=request.user.profile.dependencia,
        estado='t')
        arreglo.append({'name':'Por revisar','y':actividades.count()})
        actividades = Actividad.objects.filter(programaoperativo__dependencia=request.user.profile.dependencia,
        estado='r')
        arreglo.append({'name':'Válidas','y':actividades.count()})
        actividades = Actividad.objects.filter(programaoperativo__dependencia=request.user.profile.dependencia,
        estado='n')
        arreglo.append({'name':'No válida','y':actividades.count()})
        arreglo = json.dumps(arreglo)
        return render(request,'programasOperativos/actividades/reportesEnlace.html',{
            'actividades':arreglo
        })

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
            fecha_final = datetime.datetime.strptime(request.POST.get('fecha_fi'),'%Y-%m-%d')
            fecha_inicial = datetime.datetime.strptime(request.POST.get('fecha_in'),'%Y-%m-%d')

            junio = datetime.datetime.strptime('2019-06-30','%Y-%m-%d')
            if((fecha_final <= junio or fecha_inicial <= junio)
            and
            ((request.user.profile.dependencia.id != 14) and (request.user.profile.dependencia.id != 23)
            and (request.user.profile.dependencia.id != 12) and (request.user.profile.dependencia.id != 1)
             and (request.user.profile.dependencia.id != 22) and (request.user.profile.dependencia.id != 21)
             and (request.user.profile.dependencia.id != 11))):
                messages.error(request,'La captura anterior al 30 de junio de 2019 está inhabilitada')
                return redirect('nuevaActividad')
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
    def cambiarRuta(self,actividad):
        ruta = str(datetime.datetime.now().year) + '/' + str(datetime.datetime.now().month) + '/'
        if not os.path.exists(settings.MEDIA_ROOT + '/' + ruta):
            os.makedirs(settings.MEDIA_ROOT + '/' + ruta)
        os.rename(actividad.evidencia.path,settings.MEDIA_ROOT+'/'+ruta+str(actividad.evidencia))
        actividad.evidencia = ruta + str(actividad.evidencia)
        actividad.save()
    def get(self,request,idActividad):
        """validar si ya subió información no pueda acceder"""
        actividad = Actividad.objects.get(pk=idActividad)
        form = TerminarActividadesForm()
        # if request.user.profile.dependencia.tipo == 'd':
        #     conceptosGasto = ConceptoGasto.objects.filter(tipoDependencia='d')
        # else:
        #     conceptosGasto = ConceptoGasto.objects.filter(tipoDependencia='p',dependencia=request.user.profile.dependencia)
        # conceptosGasto = serializers.serialize('json',conceptosGasto, use_natural_foreign_keys=True)
        return render(request,'programasOperativos/actividades/terminarActividad.html',{
            'form':form,
            'actividad':actividad
        })
    def post(self,request,idActividad):
        actividad = Actividad.objects.get(pk=idActividad)
        #SI NO ES VÁLIDA LA ACTIVIDAD ELIMINA SUS DETALLES DE GASTO PARA VOLVER A CAPTURARSE
        # if actividad.estado == 'n':
        #     gastosActividad = DetallesGasto.objects.filter(actividad=actividad)
        #     gastosActividad.delete()
        form = TerminarActividadesForm(request.POST, instance=actividad)
        if form.is_valid():
            datos = form.save(commit=False)
            archivo = request.FILES['archivos']
            archivo.name = (
                str(request.user.profile.dependencia.id) + 
                '-evidencia.pdf'
                )
            datos.evidencia = archivo
            datos.estado = 't'
            save = datos.save()
            #ESTO ENTRARÍA EN UN HILO
            cambiarRuta = threading.Thread(name='cambiarRuta',target=self.cambiarRuta,args=(actividad, ))
            cambiarRuta.start()
            
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

class RevalidarActividadFormView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,idActividad):
        """validar si ya subió información no pueda acceder"""
        actividad = Actividad.objects.get(pk=idActividad)
        form = RevalidarActividadesForm(instance=actividad) 
        return render(request,'programasOperativos/actividades/revalidarActividad.html',{
            'form':form,
            'actividad':actividad
        })
    def post(self,request,idActividad):
        actividad = Actividad.objects.get(pk=idActividad)
        form = RevalidarActividadesForm(request.POST, instance=actividad)
        if form.is_valid():
            datos = form.save(commit=False)
            archivo = request.FILES['archivos']
            archivo.name = (
                str(request.user.profile.dependencia.id) + 
                '-evidencia.pdf'
                )
            datos.evidencia = archivo
            datos.estado = 't'
            save = datos.save()
            messages.success(request, 'Actividad actualizada con éxito.')
            return redirect('listActividades')
        messages.error(request, form._errors)
        actividad = Actividad.objects.get(pk=idActividad)
        form = TerminarActividadesForm()
        conceptosGasto = ConceptoGasto.objects.all()
        conceptosGasto = serializers.serialize('json',conceptosGasto, use_natural_foreign_keys=True)
        return render(request,'programasOperativos/actividades/revalidarActividad.html',{
            'form':form,
            'actividad':actividad,
            'conceptosGasto':conceptosGasto
        })

class ActividadesListView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        pos = ProgramaOperativo.objects.filter(dependencia=request.user.profile.dependencia)
        actividades = []
        for po in pos:
            actividadesPo = Actividad.objects.filter(programaoperativo=po).exclude(estado='i')
            for actividadPo in actividadesPo:
                actividades.append(actividadPo)
                pass
            pass
        return render(request,'programasOperativos/actividades/listActividades.html',{
            'actividades':actividades
        })

#Todas las vistas de admins
class ListActividadesAdmin(LoginRequiredMixin,View):
    login_url = 'login'
    def obtenerDependencias(self):
        dependencias = Dependencia.objects.filter(estado='a')
        dependencias = dependencias.order_by('nombre')
        arrDependencias = []
        for dependencia in dependencias:
            actividades = Actividad.objects.filter(estado='t',programaoperativo__dependencia=dependencia).exclude(estado='i')
            if actividades:
                dependencia.nombre += '*'
                arrDependencias.append(dependencia)
            else:
                arrDependencias.append(dependencia)
        return arrDependencias
    def get(self,request):
        if request.user.profile.tipoUsuario == 'e':
            return redirect('index')
        dependencias = self.obtenerDependencias()
        programasOperativos = ProgramaOperativo.objects.filter(estado='a').order_by('nombre') 
        # dependencias = Dependencia.objects.filter(estado='a')
        # dependencias = dependencias.order_by('nombre')
        objetivos = Objetivo.objects.filter(estado='a')
        objetivos = objetivos.order_by('nombre')
        return render(request,'programasOperativos/actividades/admin/listActividadesAdmin.html',{
            'dependencias':dependencias,
            'objetivos':objetivos,
            'programasOperativos':programasOperativos
        })
    def post(self,request):
        if request.user.profile.tipoUsuario == 'e':
            return redirect('index')
        programasOperativos = ProgramaOperativo.objects.filter(estado='a').order_by('nombre')
        dependencias = self.obtenerDependencias()
        objetivos = Objetivo.objects.filter(estado='a')
        objetivos = objetivos.order_by('nombre')
        actividades = filtroActividades(
            id_dependencia=int(request.POST.get('dependencia') if request.POST.get('dependencia') else 0),
            id_eje=request.POST.get('eje'),
            id_objetivo=int(request.POST.get('objetivo') if request.POST.get('objetivo') else 0),
            estado=request.POST.get('estado'),
            id_programaOperativo=int(request.POST.get('programaOperativo') if request.POST.get('programaOperativo') else 0)
        )
        arrayActividades = []
        for actividad in actividades:
            arrayActividades.append(actividad.id)
        arrayActividades = json.dumps(arrayActividades)
        return render(request,'programasOperativos/actividades/admin/listActividadesAdmin.html',{
            'dependencias':dependencias,
            'objetivos':objetivos,
            'actividades':actividades,
            'arrayActividades':arrayActividades,
            'programasOperativos':programasOperativos
        })

class VerActividadAdmin(LoginRequiredMixin,View):
    login_url = 'login'
    def obtenerContexto(self, idActividad):
        actividad = Actividad.objects.get(pk=idActividad)
        accion = actividad.accion
        periodoGobierno = PeriodoGobierno.objects.filter(fechaInicial__lte=actividad.fecha_in, fechaFinal__gte=actividad.fecha_in).first()
        metas = actividad.accion.meta.all()
        tieneMeta = False
        porcentajeAccion = 0
        claseSemaforo = 'danger'
        metas = actividad.accion.meta.filter(periodo=periodoGobierno)
        arregloMetas = []
        if metas:
            contadorMetas = 0
            acumuladorMetas = 0
            for meta in metas:
                if meta.meta>0:
                    contadorMetas += 1
                    #obtenemos las actividades del periodo de gobierno que son válidas
                    actividades = Actividad.objects.filter(accion=accion,estado='r',
                    fecha_fi__range=(periodoGobierno.fechaInicial,periodoGobierno.fechaFinal))
                    contadorActividades = 0
                    for actividad in actividades:
                        contadorActividades += actividad.multiplicador
                    tieneMeta = True
                    porcentajeMeta = (contadorActividades / meta.meta) * 100
                    #aquí le pones el tope al porcentaje
                    porcentajeMeta = round(porcentajeMeta,0) #if porcentajeMeta <= 100 else 100.0
                    acumuladorMetas += porcentajeMeta
            porcentajeAccion = acumuladorMetas / contadorMetas if contadorMetas > 0 else 0
            porcentajeAccion = int(porcentajeAccion)
            if porcentajeAccion > 34 and porcentajeAccion < 85:
                claseSemaforo = 'warning'
            elif porcentajeAccion >= 85:
                claseSemaforo = 'success'
        return {
            'tieneMeta':tieneMeta,
            'porcentajeMeta':porcentajeAccion,
            'claseSemaforo':claseSemaforo
                }
    def get(self, request,idActividad):
        actividad = Actividad.objects.get(pk=idActividad)
        contexto = self.obtenerContexto(idActividad)
        contexto['actividad'] = actividad
        return render(request,'programasOperativos/actividades/admin/verActividadAdmin.html',contexto)
    def post(self, request,idActividad):
        actividad = Actividad.objects.get(pk=idActividad)
        if request.POST.get('cualitativa'):
            accion = actividad.accion
            accion.cualitativa = True
            accion.save()
        if request.POST.get('estado'):
            metas = actividad.accion.meta.all()
            if not metas and not actividad.accion.cualitativa:
                messages.error(request,'Se necesita definir si la acción es cualitativa o si tiene metas')
            else:
                actividad.observaciones = request.POST.get('observaciones')
                actividad.estado = request.POST.get('estado')
                actividad.save()
                messages.success(request,'Cambio realizado con éxito')
        contexto = self.obtenerContexto(idActividad)
        contexto['actividad'] = actividad
        return render(request,'programasOperativos/actividades/admin/verActividadAdmin.html',contexto)

class ReporteActividadesAdmin(LoginRequiredMixin,View):
    login_url = 'login'
    def filtrar(self,eje):
        categories = ''
        dependencias = []
        #En este arreglo estarán todos los arreglos de todas las actividades
        arregloObjetivos = []
        objetivos = filtroObjetivos(id_eje=eje)
        #Iteramos todos los objetivos
        for objetivo in objetivos:
            categories = ''
            arreglosActividades = [{
                'name':'Programadas',
                'data':[]
            },{
                'name':'Por revisar',
                'data':[]
            },{
                'name':'Válidas',
                'data':[]
            },{
                'name':'No válida',
                'data':[]
            }]
            #Obtenemos todas las dependencias de un objetivo
            dependencias = filtroDependencias(id_objetivo=objetivo.id)

            #Cada dependencia será una categoría, las iteramos para obtener su nombre
            for dependencia in dependencias:
                categories += dependencia.nombre + '|'
                actividades = Actividad.objects.filter(
                    programaoperativo__dependencia=dependencia,
                    accion__objetivo=objetivo,
                    estado='p'
                    )
                arreglosActividades[0]['data'].append(actividades.count())
                actividades = Actividad.objects.filter(
                    programaoperativo__dependencia=dependencia,
                    accion__objetivo=objetivo,
                    estado='t'
                )
                arreglosActividades[1]['data'].append(actividades.count())
                actividades = Actividad.objects.filter(
                    programaoperativo__dependencia=dependencia,
                    accion__objetivo=objetivo,
                    estado='r'
                )
                arreglosActividades[2]['data'].append(actividades.count())
                actividades = Actividad.objects.filter(
                    programaoperativo__dependencia=dependencia,
                    accion__objetivo=objetivo,
                    estado='n'
                )
                arreglosActividades[3]['data'].append(actividades.count())

            arregloObjetivos.append({
                'title':objetivo.nombre,
                'categories':categories,
                'arregloActividades':arreglosActividades
            })
        arregloObjetivos = json.dumps(arregloObjetivos)
        return arregloObjetivos
    def get(self,request):
        if request.user.profile.tipoUsuario == 'e':
            return redirect('index')
        arregloObjetivos = self.filtrar("1")
        return render(request,'programasOperativos/actividades/admin/reporteActividadesAdmin.html',{
            'arregloObjetivos':arregloObjetivos
        })
    def post(self,request):
        if request.user.profile.tipoUsuario == 'e':
            return redirect('index')
        eje = request.POST.get('eje')
        arregloObjetivos = self.filtrar(eje)
        return render(request,'programasOperativos/actividades/admin/reporteActividadesAdmin.html',{
            'arregloObjetivos':arregloObjetivos
        })

class ProductividadAdmin(LoginRequiredMixin,View):
    def get(self,request):
        logs = LogActividad.objects.all()
        #este será el arreglo que iteraremos para obtener lo que ha hecho
        usuarios = []
        #definimos el formato que leerá la gráfica
        arreglosActividades = [{
                'name':'Validadas',
                'data':[]
            },{
                'name':'Invalidadas',
                'data':[]
            }]
        #En esta variable se concatenarán las categoráis de la gráfica
        nombres = ''
        for log in logs:
            usuarios.append(log.usuario)
            # nombres =  log.usuario.first_name + '|' + nombres
        usuarios = list(set(usuarios))
        for usuario in usuarios:
            nombres += usuario.first_name + '|'
            logs = LogActividad.objects.filter(usuario=usuario,estado='r')
            arreglosActividades[0]['data'].append(logs.count())
            logs = LogActividad.objects.filter(usuario=usuario,estado='n')
            arreglosActividades[1]['data'].append(logs.count())
        arreglosActividades = json.dumps(arreglosActividades)
        
        return render(request,'programasOperativos/actividades/admin/productividadAdmin.html',{
            'nombres':nombres,
            'arregloActividades':arreglosActividades
        })

class MetasAdmin(LoginRequiredMixin,View):
    login_url = 'login'
    queue = queue.Queue()
    def obtenerContexto(self):
        dependencias = Dependencia.objects.filter(estado='a')
        dependencias = dependencias.order_by('nombre')
        objetivos = Objetivo.objects.filter(estado='a')
        objetivos = objetivos.order_by('nombre')
        return {
            'dependencias':dependencias,
            'objetivos':objetivos
        }
    def obtenerDatosDependencia(self,queue,periodoGobierno, id_dependencia=0):
        dependencia = Dependencia.objects.get(pk=id_dependencia)
        objetoDependencia = {
        'dependencia':dependencia.nombre,
        'pos':[]
        }
        pos = filtroProgramasOperativos(id_dependencia=id_dependencia)
        for po in pos:
            objetoPo = {
                'id':po.id,
                'nombre':po.nombre,
                'acciones':[],
                'porcentajePo':0
            }
            acciones = po.acciones.all()
            acumuladorPorcentajeAccion = 0
            contadorAccionesConMeta = 0
            for accion in acciones:
                tieneMeta = False
                porcentajeAccion = 0
                claseSemaforo = 'danger'
                metas = accion.meta.filter(periodo=periodoGobierno)
                arregloMetas = []
                if metas:
                    contadorAccionesConMeta += 1
                    contadorMetas = 0
                    acumuladorMetas = 0
                    for meta in metas:
                        if meta.meta>0:
                            contadorMetas += 1
                            #obtenemos las actividades del periodo de gobierno que son válidas
                            actividades = Actividad.objects.filter(accion=accion,estado='r',
                            fecha_fi__range=(periodoGobierno.fechaInicial,periodoGobierno.fechaFinal))
                            contadorActividades = 0
                            for actividad in actividades:
                                contadorActividades += actividad.multiplicador
                            tieneMeta = True
                            porcentajeMeta = (contadorActividades / meta.meta) * 100
                            #aquí le pones el tope al porcentaje
                            porcentajeMeta = round(porcentajeMeta,2) #if porcentajeMeta <= 100 else 100.0
                            acumuladorMetas += porcentajeMeta
                            arregloMetas.append({
                                'descripcion':meta.descripcion,
                                'porcentajeMeta':porcentajeMeta
                            })
                    porcentajeAccion = acumuladorMetas / contadorMetas if contadorMetas > 0 else 0
                    acumuladorPorcentajeAccion += porcentajeAccion
                    if porcentajeAccion > 34 and porcentajeAccion < 85:
                        claseSemaforo = 'warning'
                    elif porcentajeAccion >= 85:
                        claseSemaforo = 'success'
                else:
                    continue
                objetoPo['acciones'].append({
                        'id':accion.id,
                        'nombre':accion.nombre,
                        'metas':arregloMetas,
                        # 'meta':accion.meta,
                        # 'descripcionMeta':accion.descripcionMeta,
                        'totalActividades':actividades if tieneMeta else None,
                        'porcentajeAccion':round(porcentajeAccion,1),
                        'porcentajeEnteroAccion':int(round(porcentajeAccion,1)),
                        'claseSemaforo':claseSemaforo
                })
                pass
            #porcentaje total del programa operativo
            if contadorAccionesConMeta > 0:
                porcentajePo = (acumuladorPorcentajeAccion / contadorAccionesConMeta)
                objetoPo['porcentajePo'] = round(porcentajePo,2)
                objetoDependencia['pos'].append(objetoPo)

        self.queue.put(objetoDependencia)
        return
    def filtrarDependencias(self,periodoGobierno,id_dependencia=0):
        #ESTE ES EL MODELO DE OBJETO QUE OBTENDREMOS
        arreglosDependencia = []
        dependencias = []
        #se hará lo mismo en caso de ser individual o todas las dependencias
        if id_dependencia==0:
            'hooli'
            dependencias = Dependencia.objects.filter(estado='a')
        else:
            dependencia = Dependencia.objects.get(pk=id_dependencia)
            dependencias.append(dependencia)
        #lista de hilos de consulta
        threads = []
        for dependencia in dependencias:
            hiloDatosDependencia = threading.Thread(name='datosDependencia',
            target=self.obtenerDatosDependencia,args=(self.queue,periodoGobierno,dependencia.id,))
            threads.append(hiloDatosDependencia)
            hiloDatosDependencia.start()
        for thread in threads:
            #cerramos threads por buenas prácticas
            thread.join()
            pass
        #AQUÍ TENEMOS LOS DATOS GENERADOS POR LOS HILOS
        for i in range(self.queue.qsize()):
            arreglosDependencia.append(self.queue.get())
        return arreglosDependencia
    def get(self,request):
        #se renderiza como dependencia, como objetivo, como eje
        if request.user.profile.tipoUsuario == 'e':
            return redirect('index')
        contexto = self.obtenerContexto()
        periodoGobierno = PeriodoGobierno.objects.get(pk=1)
        arreglosDependencias = self.filtrarDependencias(periodoGobierno)
        # arreglosDependencias = json.dumps(arreglosDependencias)
        contexto ['arreglosDependencias'] = arreglosDependencias
        contexto ['tipoFiltro'] = 'dependencia'
        objetivos = Objetivo.objects.filter(estado='a')
        return render(request,'programasOperativos/actividades/admin/metasAdmin.html',contexto)
    def post(self,request):
        if request.POST.get('accion'):
            programasOperativos = ProgramaOperativo.objects.filter(estado='a').order_by('nombre')
            dependencias = ListActividadesAdmin.obtenerDependencias(self)
            objetivos = Objetivo.objects.filter(estado='a')
            objetivos = objetivos.order_by('nombre')
            accion = Acciones.objects.get(pk=request.POST.get('accion'))
            actividades = Actividad.objects.filter(accion=accion)
            arrayActividades = []
            for actividad in actividades:
                arrayActividades.append(actividad.id)
            arrayActividades = json.dumps(arrayActividades)
            return render(request,'programasOperativos/actividades/admin/listActividadesAdmin.html',{
                'dependencias':dependencias,
                'objetivos':objetivos,
                'actividades':actividades,
                'arrayActividades':arrayActividades,
                'programasOperativos':programasOperativos
            })
        if request.user.profile.tipoUsuario == 'e':
            return redirect('index')
        if request.POST.get('options') == 'dependencias':
            resultado = self.filtrarDependencias()
            filtroProgramasOperativos()
        eje = request.POST.get('eje')
        contexto = self.obtenerContexto()
        return render(request,'programasOperativos/actividades/admin/metasAdmin.html',contexto)

