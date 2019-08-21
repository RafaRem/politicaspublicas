import json
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q,Count
"""funciones de otras vistas"""
from apps.dependencia.views import getGastoPeriodo
"""Modelos"""
from apps.indicador.models import PeriodoGobierno, Meta, Configuracion, Periodo
from apps.programaOperativo.models import Acciones,ProgramaOperativo,Actividad
from apps.objetivo.models import Objetivo
from apps.dependencia.models import Dependencia
"""Forms"""
from apps.indicador.forms import ConfiguracionesForm

def obtenerActividades(idAccion=0,idProgramaOperativo=0,idObjetivo=0,idDependencia=0,idEje=''):
    consulta = Q()
    consulta = Q(estado='r')
    consulta |= Q(estado='s')
    if idAccion > 0:
        accion = Acciones.objects.get(pk=idAccion)
        consulta &= Q(accion=accion)
    if idProgramaOperativo>0:
        programaOperativo = ProgramaOperativo.objects.get(pk=idProgramaOperativo)
        consulta &= Q(programaoperativo=programaOperativo)
    if idObjetivo>0:
        objetivo = Objetivo.objects.get(pk=idObjetivo)
        consulta &= Q(accion__objetivo=objetivo)
    if idDependencia>0:
        dependencia =  Dependencia.objects.get(pk=idDependencia)
        consulta &= Q(programaoperativo__dependencia=dependencia)
    if idEje != '':
        consulta &= Q(accion__objetivo__ejeTransversal=idEje)
    actividades = Actividad.objects.filter(consulta)
    return actividades

def obtenerGeoPuntosActividades(actividades):
    puntos = []
    for actividad in actividades:
        puntos.append([actividad.latitud,actividad.longitud])
    return puntos

def obtenerTotalInvolucrados(actividades):
    total = 0
    for actividad in actividades:
        if actividad.personasInvolucradas:
            total += int(actividad.personasInvolucradas) 
    return total

def obtenerPorcentajeAccion(accion,periodoGobierno):
    metas = accion.meta.all()
    tieneMeta = False
    porcentajeAccion = 0
    descripcionMeta = ''
    cantidadMeta = 0
    metas = accion.meta.filter(periodo=periodoGobierno)
    arregloMetas = []
    contadorActividades = 0
    if metas:
        contadorMetas = 0
        acumuladorMetas = 0
        for meta in metas:
            if meta.meta>0:
                contadorMetas += 1
                #obtenemos las actividades del periodo de gobierno que son válidas
                actividades = Actividad.objects.filter(accion=accion,estado='r',
                fecha_fi__range=(periodoGobierno.fechaInicial,periodoGobierno.fechaFinal))
                for actividad in actividades:
                    contadorActividades += actividad.multiplicador
                tieneMeta = True
                porcentajeMeta = (contadorActividades / meta.meta) * 100
                descripcionMeta = meta.descripcion
                cantidadMeta = meta.meta
                #aquí le pones el tope al porcentaje
                porcentajeMeta = round(porcentajeMeta,0) #if porcentajeMeta <= 100 else 100.0
                acumuladorMetas += porcentajeMeta
        porcentajeAccion = acumuladorMetas / contadorMetas if contadorMetas > 0 else 0
        porcentajeAccion = int(porcentajeAccion)
    return {
        'porcentajeAccion':porcentajeAccion,
        'contadorActividades':contadorActividades,
        'descripcionMeta':descripcionMeta
        }

def obtenerTotalBenefieciarios(actividades):
    total = 0
    for actividad in actividades:
        if actividad.beneficiarios:
            total += int(actividad.beneficiarios) 
    return total
# Create your views here.
class AccionesMetasView(LoginRequiredMixin,View):
    login_url = 'login'
    def obtenerAcciones(self):
        acciones = []
        programasOperativos = ProgramaOperativo.objects.filter(estado='a')
        for programaOperativo in programasOperativos:
            accionesPo = programaOperativo.acciones.all()
            for accion in accionesPo:
                acciones.append({
                    'accion':accion,
                    'programaOperativo':programaOperativo,
                })
        return acciones
        #Aquí les va a decir si ya se capturó meta
    def get(self,request):
        if request.user.profile.tipoUsuario == 'e':
            return redirect('index')
        periodos = PeriodoGobierno.objects.all()
        acciones_po = self.obtenerAcciones()
        return render(request,'indicadores/metas/capturarMetas.html',{
            'periodos':periodos,
            'acciones_po':acciones_po
        })

class AccionesMetasForm(LoginRequiredMixin,View):
    login_url = 'login'
    def getContexto(self,accion):
        periodos = PeriodoGobierno.objects.all()
        periodos = periodos.order_by('descripcion')
        metas = accion.meta.all()
        return {
            'accion':accion,
            'periodos':periodos,
            'metas':metas
        }
    def get(self,request,idAccion):
        if request.user.profile.tipoUsuario == 'e':
            return redirect('index')
        accion = Acciones.objects.get(pk=idAccion)
        contexto = self.getContexto(accion)
        return render(request,'indicadores/metas/capturarMetasForm.html',contexto)
    def post(self,request,idAccion):
        accion = Acciones.objects.get(pk=idAccion)
        if request.POST.get('cualitativa'):
            accion.cualitativa = True
            accion.save()
            return redirect('capturarMetasList')
        contexto = self.getContexto(accion)
        periodos = PeriodoGobierno.objects.all()
        periodos = periodos.order_by('descripcion')
        descripcionMeta = request.POST.get('descripcion')
        if descripcionMeta:
            metasForm = request.POST.getlist('meta')
            metas = []
            for i in range(0,len(periodos)):
                if metasForm[i]:
                    meta = Meta.objects.create(descripcion=descripcionMeta,meta=metasForm[i],periodo=periodos[i])
                    accion.meta.add(meta)
        if request.POST.get('eliminarMeta'):
            meta = Meta.objects.get(pk=request.POST.get('eliminarMeta'))
            meta.delete()
        return render(request,'indicadores/metas/capturarMetasForm.html',contexto)

class FichaAccion(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idAccion):
        accion = Acciones.objects.get(pk=idAccion)
        configuracion = Configuracion.objects.get(pk=1)
        actividades = obtenerActividades(
            idAccion=int(idAccion)
        )
        #los puntos son de geolicalización
        puntos = obtenerGeoPuntosActividades(actividades)
        puntos = json.dumps(puntos)
        periodosGasto = Periodo.objects.filter(fechaFinal__range=(configuracion.periodoGobierno.fechaInicial,configuracion.periodoGobierno.fechaFinal))
        gasto = 0
        for periodoGasto in periodosGasto:
            gasto += getGastoPeriodo(accion,periodoGasto)
        numeroActividades = actividades.count()
        if numeroActividades>0:
            promedioGastoActividad = round(gasto / numeroActividades,2)
        else:
            promedioGastoActividad = 0
        totalBeneficiarios = obtenerTotalBenefieciarios(actividades)
        totalInvolucrados = obtenerTotalInvolucrados(actividades)
        if numeroActividades>0:
            promedioBeneficiariosActividad = round(totalBeneficiarios / numeroActividades,0) 
        else:
            promedioBeneficiariosActividad = 0
        if numeroActividades>0:
            promedioInvolucradosActividad = round(totalInvolucrados / numeroActividades,0)
        else:
            promedioInvolucradosActividad = 0
        if totalBeneficiarios>0:
            promedioGastoBeneficairio = round(gasto / totalBeneficiarios,0)
        else:
            promedioGastoBeneficairio = 0
        porcentajeAccion = 0
        meta = {
            'tieneMeta':False,
            'porcentajeMeta':0,
            'claseSemaforo':'danger',
            'descripcionMeta':'Sin meta',
            'cantidadMeta':''
            }
        claseSemaforo = 'danger'
        if accion.cualitativa:
            claseSemaforo = 'info'
            meta = {
                'tieneMeta':False,
                'porcentajeMeta':100,
                'claseSemaforo':claseSemaforo,
                'descripcionMeta':'meta cualitativa',
                'cantidadMeta':''
             }
        elif accion.meta.all():
            resultadoAccion = obtenerPorcentajeAccion(accion,configuracion.periodoGobierno)
            if resultadoAccion['porcentajeAccion'] > 34 and resultadoAccion['porcentajeAccion'] < 85:
                claseSemaforo = 'warning'
            elif resultadoAccion['porcentajeAccion'] >= 85:
                claseSemaforo = 'success'
            meta = accion.meta.filter(periodo=configuracion.periodoGobierno).first()
            meta = {
                'tieneMeta':True,
                'porcentajeMeta':resultadoAccion['porcentajeAccion'],
                'claseSemaforo':claseSemaforo,
                'descripcionMeta':meta.descripcion,
                'cantidadMeta':resultadoAccion['contadorActividades']
            }
        return render(request,'indicadores/fichaAccion.html',{
            'accion':accion,
            'puntos':puntos,
            'numeroActividades':numeroActividades,
            'promedioGastoActividad':promedioGastoActividad,
            'promedioGastoBeneficairio':promedioGastoBeneficairio,
            'totalBeneficiarios':totalBeneficiarios,
            'totalInvolucrados':totalInvolucrados,
            'promedioBeneficiariosActividad':promedioBeneficiariosActividad,
            'promedioInvolucradosActividad':promedioInvolucradosActividad,
            'meta':meta,
            'gasto':gasto
        })

class FichaProgramaOperativo(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idPrograma):
        programaOperativo = ProgramaOperativo.objects.get(pk=idPrograma)
        configuracion = Configuracion.objects.get(pk=1)
        actividades = obtenerActividades(
            idProgramaOperativo=int(idPrograma)
        )
        #los puntos son de geolicalización
        puntos = obtenerGeoPuntosActividades(actividades)
        puntos = json.dumps(puntos)
        acciones = programaOperativo.acciones.all()
        gasto = 0
        periodosGasto = Periodo.objects.filter(fechaFinal__range=(configuracion.periodoGobierno.fechaInicial,configuracion.periodoGobierno.fechaFinal))
        for accion in acciones:
            for periodoGasto in periodosGasto:
                gasto += getGastoPeriodo(accion,periodoGasto)
        numeroActividades = actividades.count()
        if numeroActividades>0:
            promedioGastoActividad = round(gasto / numeroActividades,2)
        else:
            promedioGastoActividad = 0
        totalBeneficiarios = obtenerTotalBenefieciarios(actividades)
        totalInvolucrados = obtenerTotalInvolucrados(actividades)
        if numeroActividades>0:
            promedioBeneficiariosActividad = round(totalBeneficiarios / numeroActividades,0) 
        else:
            promedioBeneficiariosActividad = 0
        if numeroActividades>0:
            promedioInvolucradosActividad = round(totalInvolucrados / numeroActividades,0)
        else:
            promedioInvolucradosActividad = 0
        if totalBeneficiarios>0:
            promedioGastoBeneficairio = round(gasto / totalBeneficiarios,0)
        else:
            promedioGastoBeneficairio = 0
        metas = []
        acumuladorMetas = 0
        contadorMetas = 0
        for accion in acciones:
            porcentajeAccion = 0
            claseSemaforo = 'danger'
            if accion.cualitativa:
                claseSemaforo = 'info'
                metas.append({
                'accion':accion.nombre,
                'accion_id':accion.id,
                'tieneMeta':False,
                'porcentajeMeta':100,
                'claseSemaforo':claseSemaforo,
                'descripcionMeta':'meta cualitativa',
                'cantidadMeta':''
                })
            else:
                resultadoAccion = obtenerPorcentajeAccion(accion,configuracion.periodoGobierno)
                contadorMetas += 1
                acumuladorMetas += resultadoAccion['porcentajeAccion']
                if resultadoAccion['porcentajeAccion'] > 34 and resultadoAccion['porcentajeAccion'] < 85:
                    claseSemaforo = 'warning'
                elif resultadoAccion['porcentajeAccion'] >= 85:
                    claseSemaforo = 'success'
                metas.append({
                'accion':accion.nombre,
                'accion_id':accion.id,
                'tieneMeta':True,
                'porcentajeMeta':resultadoAccion['porcentajeAccion'],
                'claseSemaforo':claseSemaforo,
                'descripcionMeta':resultadoAccion['descripcionMeta'],
                'cantidadMeta':resultadoAccion['contadorActividades']
                })
        metas = json.dumps(metas)
        if contadorMetas>0:
            porcentajePo = round(acumuladorMetas / contadorMetas,2)
        else:
            porcentajePo = 0
        enteroPorcentajePo = int(porcentajePo)
        claseSemaforo = 'danger'
        if porcentajePo > 34 and porcentajePo < 85:
            claseSemaforo = 'warning'
        elif porcentajePo >= 85:
            claseSemaforo = 'success'
        return render(request,'indicadores/fichaProgramaOperativo.html',{
            'programaOperativo':programaOperativo,
            'puntos':puntos,
            'numeroActividades':numeroActividades,
            'promedioGastoActividad':promedioGastoActividad,
            'promedioGastoBeneficairio':promedioGastoBeneficairio,
            'totalBeneficiarios':totalBeneficiarios,
            'totalInvolucrados':totalInvolucrados,
            'promedioBeneficiariosActividad':promedioBeneficiariosActividad,
            'promedioInvolucradosActividad':promedioInvolucradosActividad,
            'porcentajePo':porcentajePo,
            'enteroPorcentajePo':enteroPorcentajePo,
            'claseSemaforo':claseSemaforo,
            'metas':metas,
            'gasto':gasto
        })

class FichasAdmin(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        #TO:DO quitar cuando se haga genérico
        #TO:DO definir cabeceras base y hacerlo dinámico, dependendiendo de lo que elija
        programasOperativos = ProgramaOperativo.objects.filter(estado='a')
        acciones_po = []
        for programaOperativo in programasOperativos:
            accionesPo = programaOperativo.acciones.all()
            for accion in accionesPo:
                acciones_po.append({
                    'accion':accion,
                    'programaOperativo':programaOperativo,
                })
        return render(request,'indicadores/admin/fichasAdmin.html',{
            'acciones_po':acciones_po
        })
    def post(self,request):
        return render(request,'indicadores/admin/fichasAdmin.html')

class Configuraciones(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        try:
            configuracion = Configuracion.objects.get(pk=1)
        except:
            configuracion = Configuracion.objects.create(pk=1)
            configuracion.save()
            pass
        form = ConfiguracionesForm(instance=configuracion)
        return render(request,'indicadores/configuraciones.html',{
            'form':form
        })
    def post(self,request):
        configuracion = Configuracion.objects.get(pk=1)
        form = ConfiguracionesForm(request.POST,instance=configuracion)
        if form.is_valid():
            form.save()
        return render(request,'indicadores/configuraciones.html',{
            'form':form
        })
