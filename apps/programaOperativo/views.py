import json
from datetime import datetime
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
from apps.users.views import *
"""Forms"""
from apps.users.forms import RegistrarActividad
from apps.programaOperativo.forms import ProgramaOperativoForm, ActividadesForm, TerminarActividadesForm, RevalidarActividadesForm
"""Modelos"""
from apps.programaOperativo.models import ProgramaOperativo, Acciones, Actividad, DetallesGasto, LogActividad, BeneficiariosActividad, MetaAccion,VariableActividad
from apps.objetivo.models import Objetivo
from apps.indicador.models import ConceptoGasto, ClasificacionGasto,Periodo,PeriodoGobierno, Configuracion, Variable
from apps.dependencia.models import Dependencia, Alcance
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
    variablesActividad = VariableActividad.objects.filter(actividad=actividad)
    alcancesActividad = BeneficiariosActividad.objects.filter(actividad=actividad)
    return render(request,'programasOperativos/actividades/verActividad.html',{
        'actividad':actividad,
        'variablesActividad':variablesActividad,
        'alcancesActividad':alcancesActividad
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

class EditarMetasView(LoginRequiredMixin,View):
    login_url = 'login'
    def getContext(self,idAccion):
        accion = Acciones.objects.get(pk=idAccion)
        configuracion = Configuracion.objects.get(pk=1)
        variables = Variable.objects.all()
        periodoGobierno = configuracion.periodoGobierno
        metasAccion = MetaAccion.objects.filter(accion=accion,periodoGobierno=periodoGobierno)
        variablesMeta = []
        for metaAccion in metasAccion:
            variablesMeta.append(metaAccion.variable)
        #Quitamos las que ya están seleccionadas de las variables disponibles
        variables = Variable.objects.filter(~Q(id__in=[o.id for o in variablesMeta]))
        return {
            'metasAccion':metasAccion,
            'accion':accion,
            'variables': variables,
            'periodoGobierno':periodoGobierno
        }
    def get(self,request,idAccion):
        contexto = self.getContext(idAccion)
        return render(request,'programasOperativos/capturarMetas.html',context=contexto)
    def post(self,request,idAccion):
        accion = Acciones.objects.get(pk=idAccion)
        configuracion = Configuracion.objects.get(pk=1)
        entradas = request.POST.getlist('cantidadVariable')
        periodoGobierno = configuracion.periodoGobierno
        #Eliminas todas las metas previamente para limpiar en caso
        #de que se deseleccione alguna
        MetaAccion.objects.filter(accion=accion,
        periodoGobierno=periodoGobierno).delete()
        for entrada in entradas:
            entrada = entrada.split('-')
            idVariable = entrada[0]
            cantidad = entrada[1]
            variable = Variable.objects.get(pk=idVariable)
            try:
                MetaAccion.objects.create(
                accion=accion,
                variable=variable,
                periodoGobierno=periodoGobierno,
                cantidad=cantidad
                )
            except:
                MetaAccion.objects.update(
                accion=accion,
                variable=variable,
                periodoGobierno=periodoGobierno,
                cantidad=cantidad
                )
                pass
        contexto = self.getContext(idAccion)
        return render(request,'programasOperativos/capturarMetas.html',contexto)

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
    def get(self,request,idProgramaOperativo):
        programaOperativo = ProgramaOperativo.objects.get(pk=idProgramaOperativo)
        form = ActividadesForm()
        programasOperativos = ProgramaOperativo.objects.filter(
            dependencia=request.user.profile.dependencia.id
            )
        #Get acciones dependencia
        dependencia = request.user.profile.dependencia
        pos = ProgramaOperativo.objects.filter(dependencia=dependencia)
        acciones = []
        for po in pos:
            acciones.extend(po.acciones.all())
        #Las acciones con meta
        metasAcciones = []
        for accion in acciones:
            metasAcciones.extend(MetaAccion.objects.filter(accion=accion))
        #Hacemos un arreglo de solo las variables que tienen metas
        variablesMeta = []
        for metaAccion in metasAcciones:
            variablesMeta.append(metaAccion.variable)
        #Se quitan las repetidas
        variablesMeta = list(set(variablesMeta))
        #variables = Variable.objects.filter(~Q(id__in=[o.id for o in variablesMeta]))
        variables = Variable.objects.all()
        return render(request,'programasOperativos/actividades/actividadForm.html',{
            'form':form,
            'programaOperativo':programaOperativo,
            'variablesMeta':variablesMeta,
            'variables':variables
        })
    def post(self,request,idProgramaOperativo):
        programaOperativo = ProgramaOperativo.objects.get(pk=idProgramaOperativo)
        form = ActividadesForm(request.POST)
        if form.is_valid():
            datos = form.save(commit=False)
            accion = Acciones.objects.get(id=request.POST.get('accion'))
            datos.accion = accion
            datos.programaoperativo = programaOperativo
            datos.user = request.user
            datos.latitud = request.POST.get('latitud')
            datos.longitud = request.POST.get('longitud')
            datos.fecha_in = request.POST.get('fecha_in')
            datos.fecha_fi = request.POST.get('fecha_fi')
            fecha_final = datetime.strptime(request.POST.get('fecha_fi'),'%Y-%m-%d')
            fecha_inicial = datetime.strptime(request.POST.get('fecha_in'),'%Y-%m-%d')
            junio = datetime.strptime('2019-06-30','%Y-%m-%d')
            save = datos.save()
            actividad = Actividad.objects.latest('created')
            idActividad = actividad.id
            #guardamos las variables con su cantidad
            cantidadesVariables = request.POST.getlist('cantidadVariable')
            for cantidadVariable in cantidadesVariables:
                #posicion 0=variableID 1=Cantidad
                cantidadVariable = cantidadVariable.split('-')
                variable = Variable.objects.get(pk=cantidadVariable[0])
                cantidad = cantidadVariable[1]
                VariableActividad.objects.create(variable=variable,cantidad=cantidad,actividad=actividad)
            #****
            messages.success(request, 'Actividad registrada con éxito.')
            url = reverse('terminarActividad',args=(idActividad,))
            return redirect(url)
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
        ruta = str(datetime.now().year) + '/' + str(datetime.now().month) + '/'
        if not os.path.exists(settings.MEDIA_ROOT + '/' + ruta):
            os.makedirs(settings.MEDIA_ROOT + '/' + ruta)
        os.rename(actividad.evidencia.path,settings.MEDIA_ROOT+'/'+ruta+str(actividad.evidencia))
        actividad.evidencia = ruta + str(actividad.evidencia)
        actividad.save()
    def get(self,request,idActividad):
        """validar si ya subió información no pueda acceder"""
        actividad = Actividad.objects.get(pk=idActividad)
        form = TerminarActividadesForm(instance=actividad)
        alcancesPredefinidos = actividad.programaoperativo.dependencia.alcance.all()
        alcancesTodos = Alcance.objects.all()
        return render(request,'programasOperativos/actividades/terminarActividad.html',{
            'form':form,
            'actividad':actividad,
            'alcancesPredefinidos': alcancesPredefinidos,
            'alcancesTodos': alcancesTodos
        })
    def post(self,request,idActividad):
        actividad = Actividad.objects.get(pk=idActividad)
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
            alcances = request.POST.getlist('cantidadAlcance')
            for alcance in alcances:
                #la posición 0 es el id, el otro es la cantidad
                alcanceValues =alcance.split('-')
                alcance = Alcance.objects.get(id=alcanceValues[0])
                alcanceDependencia = actividad.programaoperativo.dependencia.alcance.filter(pk=alcance.id)
                if not alcanceDependencia:
                    actividad.programaoperativo.dependencia.alcance.add(alcance)
                BeneficiariosActividad.objects.update_or_create(
                    alcance=alcance,
                    cantidad=alcanceValues[1],
                    actividad=actividad
                    )
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
            'actividad':actividad
        })

class RevalidarActividadFormView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,idActividad):
        """validar si ya subió información no pueda acceder"""
        actividad = Actividad.objects.get(pk=idActividad)
        form = RevalidarActividadesForm(instance=actividad) 
        variablesActividad = VariableActividad.objects.filter(actividad=actividad)
        alcancesActividad = BeneficiariosActividad.objects.filter(actividad=actividad)
        #Quitamos las que ya están seleccionadas de las variables disponibles
        variablesTodas = Variable.objects.filter(~Q(id__in=[o.variable.id for o in variablesActividad]))
        alcancesTodos = Alcance.objects.filter(~Q(id__in=[o.alcance.id for o in alcancesActividad]))
        return render(request,'programasOperativos/actividades/revalidarActividad.html',{
            'form':form,
            'actividad':actividad,
            'alcancesTodos': alcancesTodos,
            'variablesTodas':variablesTodas,
            'variablesActividad':variablesActividad,
            'alcancesActividad':alcancesActividad
        })
    def post(self,request,idActividad):
        actividad = Actividad.objects.get(pk=idActividad)
        form = RevalidarActividadesForm(request.POST, instance=actividad)
        if form.is_valid():
            datos = form.save(commit=False)
            keepEvidence = request.POST.get('keepEvidence')
            #si el usuario desea conservar su evidencia, lo hace
            if keepEvidence != 'on':
                archivo = request.FILES['archivos']
                archivo.name = (
                    str(request.user.profile.dependencia.id) + 
                    '-evidencia.pdf'
                    )
                datos.evidencia = archivo
            #variables y alcances
            variables =  request.POST.getlist('cantidadVariable')
            VariableActividad.objects.filter(actividad=actividad).delete()
            for variable in variables:
                variable = variable.split('-')
                cantidad = variable[1]
                variable = Variable.objects.get(pk=variable[0])
                try:
                    VariableActividad.objects.create(
                    actividad=actividad,
                    variable=variable,
                    cantidad=cantidad
                    )
                except:
                    VariableActividad.objects.update(
                    actividad=actividad,
                    variable=variable,
                    cantidad=cantidad
                    )
                    pass
            alcances = request.POST.getlist('cantidadAlcance')
            BeneficiariosActividad.objects.filter(actividad=actividad).delete()
            for alcance in alcances:
                alcance = alcance.split('-')
                cantidad = alcance[1]
                alcance = Alcance.objects.get(pk=alcance[0])
                try:
                    BeneficiariosActividad.objects.create(
                    actividad=actividad,
                    alcance=alcance,
                    cantidad=cantidad
                    )
                except:
                    BeneficiariosActividad.objects.update(
                    actividad=actividad,
                    alcance=alcance,
                    cantidad=cantidad
                    )
                    pass
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
    def getContext(self,request,fechaInicial="",fechaFinal="",
        programaOperativoId="", estado=""):
        q = Q()
        programasOperativos = ProgramaOperativo.objects.filter(dependencia=request.user.profile.dependencia)
        if programaOperativoId=="0" or request.method == "GET":
            for po in programasOperativos:
                q |= Q(programaoperativo=po)
        else:
            programaOperativo = ProgramaOperativo.objects.get(pk=programaOperativoId)
            q &= Q(programaoperativo=programaOperativo)
        if estado != "":
            q &= Q(estado=estado)
        if fechaInicial!="" and fechaFinal!="":
            q &= Q(fecha_fi__range=(fechaInicial,fechaFinal))
        actividades = Actividad.objects.filter(q)
        return {
            'actividades':actividades,
            'programasOperativos':programasOperativos
        }
    def get(self,request):
        context = self.getContext(request)
        return render(request,'programasOperativos/actividades/listActividades.html',context)
    def post(self,request):
        programaOperativoId = request.POST.get('programaOperativo')
        estado = request.POST.get('estado')
        fecha_in = request.POST.get('fecha_in')
        fecha_fi = request.POST.get('fecha_fi')
        context = self.getContext(request,fecha_in,fecha_fi,programaOperativoId,estado)
        return render(request,'programasOperativos/actividades/listActividades.html',context)

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
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's'):
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
        descripcionMeta = ''
        cantidadMeta = 0
        metas = actividad.accion.meta.filter(periodo=periodoGobierno)
        arregloMetas = []
        variablesActividad = VariableActividad.objects.filter(actividad=actividad)
        alcancesActividad = BeneficiariosActividad.objects.filter(actividad=actividad)
        #TO:DO BORRAR LA PARTE DE METAS
        if metas:
            contadorMetas = 0
            acumuladorMetas = 0
            tieneMeta = True
            for meta in metas:
                if meta.meta>0:
                    contadorMetas += 1
                    #obtenemos las actividades del periodo de gobierno que son válidas
                    actividades = Actividad.objects.filter(accion=accion,estado='r',
                    fecha_fi__range=(periodoGobierno.fechaInicial,periodoGobierno.fechaFinal))
                    contadorActividades = 0
                    for actividad in actividades:
                        contadorActividades += actividad.multiplicador
                    porcentajeMeta = (contadorActividades / meta.meta) * 100
                    descripcionMeta = meta.descripcion
                    cantidadMeta = meta.meta
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
            'claseSemaforo':claseSemaforo,
            'descripcionMeta':descripcionMeta,
            'cantidadMeta':cantidadMeta,
            'variablesActividad':variablesActividad,
            'alcancesActividad':alcancesActividad
                }
    def get(self, request,idActividad):
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's'):
            return redirect('index')
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
            # if not metas and not actividad.accion.cualitativa:
            #     messages.error(request,'Se necesita definir si la acción es cualitativa o si tiene metas')
            # else:
            actividad.observaciones = request.POST.get('observaciones')
            actividad.estado = request.POST.get('estado')
            actividad.multiplicador = 1
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
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's'):
            return redirect('index')
        arregloObjetivos = self.filtrar("1")
        return render(request,'programasOperativos/actividades/admin/reporteActividadesAdmin.html',{
            'arregloObjetivos':arregloObjetivos
        })
    def post(self,request):
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's'):
            return redirect('index')
        eje = request.POST.get('eje')
        arregloObjetivos = self.filtrar(eje)
        return render(request,'programasOperativos/actividades/admin/reporteActividadesAdmin.html',{
            'arregloObjetivos':arregloObjetivos
        })

class ProductividadAdmin(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        if ((request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's')):
            return redirect('index')
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
        'dependencia_id':dependencia.id,
        'porcentaje':0.0,
        'porcentajeEntero':0,
        'claseSemaforo':'info',
        'pos':[]
        }
        pos = filtroProgramasOperativos(id_dependencia=id_dependencia)
        acumuladorPorcentajesPo = 0.0
        contadorPos = 0
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
                contadorPos += 1
                porcentajePo = (acumuladorPorcentajeAccion / contadorAccionesConMeta)
                acumuladorPorcentajesPo += round(porcentajePo,2)
                objetoPo['porcentajePo'] = round(porcentajePo,2)
                objetoDependencia['pos'].append(objetoPo)
        porcentajeDependencia = round(acumuladorPorcentajesPo / contadorPos,2) if contadorPos > 0 else 0
        objetoDependencia['porcentaje'] = porcentajeDependencia
        objetoDependencia['porcentajeEntero'] = int(porcentajeDependencia)
        if objetoDependencia['porcentajeEntero'] > 34 and objetoDependencia['porcentajeEntero'] < 85:
            claseSemaforo = 'warning'
        elif objetoDependencia['porcentajeEntero'] >= 85:
            claseSemaforo = 'success'
        objetoDependencia['claseSemaforo'] = claseSemaforo
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
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's') and (request.user.profile.tipoUsuario != 'i'):
            return redirect('index')
        contexto = self.obtenerContexto()
        #TO:DO esto tiene que ser cambiado por una tabla de configuraciones
        configuracion = Configuracion.objects.get(pk=1)
        arreglosDependencias = self.filtrarDependencias(configuracion.periodoGobierno)
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
            actividades = Actividad.objects.filter(Q(estado='r') | Q(estado='s'))
            actividades = actividades.filter(accion=accion)
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

@login_required(login_url='login')
def escoger_po(request):
    arrayPosActs = []
    programasOperativos = ProgramaOperativo.objects.filter(
        dependencia=request.user.profile.dependencia,
        estado='a'
        )
    for po in programasOperativos:
        actividades = Actividad.objects.filter(~Q(estado='i'),Q(programaoperativo=po))
        arrayPosActs.append({
            'idPo':po.id,
            'nombrePo':po.nombre,
            'numeroActividades':actividades.count()
        })
    return render(request,"programasOperativos/actividades/escogerPo.html",{
        'arrayPosActs':arrayPosActs
    })

