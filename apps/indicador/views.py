import json
import random
from django.core import serializers
from datetime import datetime, timedelta
from collections import OrderedDict
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

def obtenerMesesGobierno():
    dates = ["2018-11-01", "2019-08-30"]
    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    meses = []
    mesesDict = OrderedDict(((start + timedelta(_)).strftime(r"%b-%y"), None) for _ in range((end - start).days)).keys()
    for mes in mesesDict:
        meses.append(mes)
    return meses

def obtenerDependenciasPos(programasOperativos):
    dependencias = []
    for programaOperativo in programasOperativos:
        dependencias.append(programaOperativo.dependencia)
    return list(set(dependencias))

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

def obtenerComparacionActividades(programasOperativos,filtrarPor):
    """Opciones: 'd' = dependencias, 'o' = objetivo. programasOperativos es un arreglo de programas operativos a comparar"""
    datos = []
    if filtrarPor == 'd':
        dependencias = obtenerDependenciasPos(programasOperativos)
        for dependencia in dependencias:
            contadorActividades = 0
            for programaOperativo in programasOperativos:
                if programaOperativo.dependencia == dependencia:
                    actividades = obtenerActividades(idProgramaOperativo=programaOperativo.id)
                    contadorActividades += actividades.count()
            random_number = random.randint(0,16777215)
            hex_number = str(hex(random_number))
            color ='#'+ hex_number[2:]
            datos.append([dependencia.nombre, contadorActividades, color, dependencia.nombre])
        return datos 

def obtenerComparacionActividadesMeses(arreglo,filtrarPor,xAxis,yAxis):
    """Opciones: 'd' = dependencias, 'o' = objetivo. programasOperativos es un arreglo de programas operativos a comparar"""
    resultado = []
    #El arreglo por parametro contiene programasOperativos
    for x,valx in enumerate(xAxis):
        for y,valy in enumerate(yAxis):
            fechaDesde = datetime.strptime(valy, r"%b-%y")
            mesHasta = fechaDesde.month
            if mesHasta == 12:
                mesHasta = 1
            else:
                mesHasta += 1
            fechaHasta = fechaDesde.replace(month=mesHasta)
            if filtrarPor =='d':
                actividades = Actividad.objects.filter(programaoperativo__dependencia=valx,
                fecha_fi__gte=fechaDesde,fecha_fi__lte=fechaHasta)
                resultado.append([x,y,actividades.count()])                
    return resultado


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

class PorcentajesMetas():
    def obtenerPorcentajeAccion(self, idAccion):
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
        gasto = round(gasto,2)
        numeroActividades = actividades.count()
        promedioGastoActividad = round(gasto / numeroActividades,2) if numeroActividades>0 else 0
        totalBeneficiarios = obtenerTotalBenefieciarios(actividades)
        totalInvolucrados = obtenerTotalInvolucrados(actividades)
        promedioBeneficiariosActividad = round(totalBeneficiarios / numeroActividades,0) if numeroActividades>0 else 0
        promedioInvolucradosActividad = round(totalInvolucrados / numeroActividades,0) if numeroActividades>0 else 0
        promedioGastoBeneficairio = round(gasto / totalBeneficiarios,0) if totalBeneficiarios>0 else 0
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
        elif accion.meta.filter(periodo=configuracion.periodoGobierno).first():
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
        accion = {
            'id':accion.id,
            'nombre':accion.nombre
        }
        return {
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
        }
    def obtenerPorcentajeProgramaOperativo(self, idPrograma):
        programaOperativo = ProgramaOperativo.objects.get(pk=idPrograma)
        acciones = programaOperativo.acciones.all()
        puntos = []
        porcentajesAcciones = []
        numeroActividades = 0
        gasto = 0
        totalBeneficiarios = 0
        totalInvolucrados = 0
        promedioBeneficiariosActividad = 0
        promedioInvolucradosActividad = 0
        porcentajePo = 0
        acumuladorPorcentajeAcciones = 0
        promedioGastoActividad = 0
        tieneMetaCuantitativa = False
        for accion in acciones:
            porcentajePo = 100 if accion.cualitativa == True else 0
            porcentajeAccion = self.obtenerPorcentajeAccion(accion.id)
            acumuladorPorcentajeAcciones += porcentajeAccion['meta']['porcentajeMeta']
            puntos.extend(json.loads(porcentajeAccion['puntos']))
            numeroActividades += porcentajeAccion['numeroActividades']
            gasto += porcentajeAccion['gasto']
            totalBeneficiarios += porcentajeAccion['totalBeneficiarios']
            totalInvolucrados += porcentajeAccion['totalInvolucrados']
            if porcentajeAccion['meta']['claseSemaforo'] != 'info':
                tieneMetaCuantitativa = True
            porcentajesAcciones.append(porcentajeAccion)
        porcentajePo = round(acumuladorPorcentajeAcciones / len(porcentajesAcciones),2) if len(porcentajesAcciones) > 0 else 0
        enteroPorcentajePo = int(porcentajePo)
        promedioGastoBeneficairio = round(gasto / totalBeneficiarios,2) if totalBeneficiarios >0 else 0
        if numeroActividades >0:
            promedioBeneficiariosActividad = int(totalBeneficiarios / numeroActividades) 
            promedioInvolucradosActividad = int(totalInvolucrados / numeroActividades)
            promedioGastoActividad = round(gasto / numeroActividades,2)
        claseSemaforo = 'danger'
        if porcentajePo > 34 and porcentajePo < 85:
            claseSemaforo = 'warning'
        elif porcentajePo >= 85:
            claseSemaforo = 'success'
        puntos = json.dumps(puntos)
        porcentajesAcciones = json.dumps(porcentajesAcciones)
        programaOperativo = {
            'id':programaOperativo.id,
            'nombre':programaOperativo.nombre,
            'dependencia':{
                'id':programaOperativo.dependencia.id,
                'nombre':programaOperativo.dependencia.nombre
            }
        }
        return {
            'programaOperativo':programaOperativo,
            'tieneMetaCuantitativa':tieneMetaCuantitativa,
            'porcentajesAcciones':porcentajesAcciones,#nota: este reemplazó a 'metas'
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
            'claseSemaforo':claseSemaforo, #pendiente
            'gasto':gasto
        }
    def obtenerPorcentajeDependencia(self, idDependencia):
        dependencia = Dependencia.objects.get(pk=idDependencia)
        programasOperativos = ProgramaOperativo.objects.filter(dependencia=dependencia)
        puntos = []
        porcentajesProgramasOperativos = []
        numeroActividades = 0
        gasto = 0
        totalBeneficiarios = 0
        totalInvolucrados = 0
        promedioBeneficiariosActividad = 0
        porcentajeDireccion = 0
        acumuladorPorcentajesPos = 0
        porcentajeProgramaOperativo = 0
        promedioInvolucradosActividad = 0
        promedioGastoActividad = 0
        tieneMetaCuantitativa = False
        for programaOperativo in programasOperativos:
            porcentajeProgramaOperativo= self.obtenerPorcentajeProgramaOperativo(programaOperativo.id)
            porcentajeDireccion = 100 if porcentajeProgramaOperativo['tieneMetaCuantitativa'] == False else 0
            tieneMetaCuantitativa = True if porcentajeProgramaOperativo['tieneMetaCuantitativa'] else False
            acumuladorPorcentajesPos += porcentajeProgramaOperativo['porcentajePo']
            puntos.extend(json.loads(porcentajeProgramaOperativo['puntos']))
            numeroActividades += porcentajeProgramaOperativo['numeroActividades']
            gasto += porcentajeProgramaOperativo['gasto']
            totalBeneficiarios += porcentajeProgramaOperativo['totalBeneficiarios']
            totalInvolucrados += porcentajeProgramaOperativo['totalInvolucrados']
            porcentajesProgramasOperativos.append(porcentajeProgramaOperativo)
        porcentajeDireccion = round(acumuladorPorcentajesPos / len(porcentajesProgramasOperativos),2) if len(porcentajesProgramasOperativos) > 0 else 0
        enteroPorcentajeDireccion = int(porcentajeDireccion)
        promedioGastoBeneficairio = round(gasto / totalBeneficiarios,2) if totalBeneficiarios >0 else 0
        if numeroActividades >0:
            promedioBeneficiariosActividad = int(totalBeneficiarios / numeroActividades) 
            promedioInvolucradosActividad = int(totalInvolucrados / numeroActividades)
            promedioGastoActividad = round(gasto / numeroActividades,2)
        claseSemaforo = 'danger'
        if porcentajeDireccion > 34 and porcentajeDireccion < 85:
            claseSemaforo = 'warning'
        elif porcentajeDireccion >= 85:
            claseSemaforo = 'success'
        puntos = json.dumps(puntos)
        porcentajesProgramasOperativos = json.dumps(porcentajesProgramasOperativos)
        dependencia ={
            'nombre':dependencia.nombre,
            'id':dependencia.id
        }
        return {
            'dependencia':dependencia,
            'tieneMetaCuantitativa':tieneMetaCuantitativa,
            'puntos':puntos,
            'numeroActividades':numeroActividades,
            'promedioGastoActividad':promedioGastoActividad,
            'promedioGastoBeneficairio':promedioGastoBeneficairio,
            'totalBeneficiarios':totalBeneficiarios,
            'totalInvolucrados':totalInvolucrados,
            'promedioBeneficiariosActividad':promedioBeneficiariosActividad,
            'promedioInvolucradosActividad':promedioInvolucradosActividad,
            'porcentajeDireccion':porcentajeDireccion,
            'enteroPorcentajeDireccion':enteroPorcentajeDireccion,
            'claseSemaforo':claseSemaforo,
            'porcentajesProgramasOperativos':porcentajesProgramasOperativos,#nota: este reemplazó a 'metas'
            'gasto':gasto
        }
    def obtenerPorcentajeObjetivo(self,idObjetivo):
        meses = obtenerMesesGobierno()
        objetivo = Objetivo.objects.get(pk=idObjetivo)
        programasOperativos__acciones = ProgramaOperativo.acciones.through.objects.filter(acciones__objetivo=objetivo)
        programasOperativos = []
        dependencias = []
        for po_accion in programasOperativos__acciones:
            programaOperativo = ProgramaOperativo.objects.get(pk=po_accion.programaoperativo_id)
            programasOperativos.append(programaOperativo)
            dependencias.append(programaOperativo.dependencia)
        dependencias = list(set(dependencias))
        programasOperativos = list(set(programasOperativos))
        tablaCalorMesesActividades = obtenerComparacionActividadesMeses(programasOperativos,'d',dependencias,meses)
        tablaCalorMesesActividades = json.dumps(tablaCalorMesesActividades)
        tablaCalorDependencias = []
        for dependencia in dependencias:
            tablaCalorDependencias.append(dependencia.nombre)
        tablaCalorDependencias = json.dumps(tablaCalorDependencias)
        tablaCalorMeses = json.dumps(meses)
        puntos = []
        porcentajesProgramasOperativos = []
        numeroActividades = 0
        gasto = 0
        totalBeneficiarios = 0
        totalInvolucrados = 0
        promedioBeneficiariosActividad = 0
        acumuladorPorcentajesDependencias = 0
        porcentajeProgramaOperativo = 0
        promedioInvolucradosActividad = 0
        promedioGastoActividad = 0
        porcentajeObjetivo = 0
        for programaOperativo in programasOperativos:
            porcentajeProgramaOperativo= self.obtenerPorcentajeProgramaOperativo(programaOperativo.id)
            porcentajeObjetivo = 100 if porcentajeProgramaOperativo['tieneMetaCuantitativa'] == False else 0
            tieneMetaCuantitativa = True if porcentajeProgramaOperativo['tieneMetaCuantitativa'] else False
            acumuladorPorcentajesDependencias += porcentajeProgramaOperativo['porcentajePo']
            puntos.extend(json.loads(porcentajeProgramaOperativo['puntos']))
            numeroActividades += porcentajeProgramaOperativo['numeroActividades']
            gasto += porcentajeProgramaOperativo['gasto']
            totalBeneficiarios += porcentajeProgramaOperativo['totalBeneficiarios']
            totalInvolucrados += porcentajeProgramaOperativo['totalInvolucrados']
            porcentajesProgramasOperativos.append(porcentajeProgramaOperativo)
        gasto = round(gasto,2)
        porcentajeObjetivo = round(acumuladorPorcentajesDependencias / len(porcentajesProgramasOperativos),2) if len(porcentajesProgramasOperativos) > 0 else 0
        enteroPorcentajeObjetivo = int(porcentajeObjetivo)
        promedioGastoBeneficairio = round(gasto / totalBeneficiarios,2) if totalBeneficiarios >0 else 0
        if numeroActividades >0:
            promedioBeneficiariosActividad = int(totalBeneficiarios / numeroActividades) 
            promedioInvolucradosActividad = int(totalInvolucrados / numeroActividades)
            promedioGastoActividad = round(gasto / numeroActividades,2)
        claseSemaforo = 'danger'
        if porcentajeObjetivo > 34 and porcentajeObjetivo < 85:
            claseSemaforo = 'warning'
        elif porcentajeObjetivo >= 85:
            claseSemaforo = 'success'
        puntos = json.dumps(puntos)
        porcentajesProgramasOperativos = json.dumps(porcentajesProgramasOperativos)
        objetivo ={
            'nombre':objetivo.nombre,
            'id':objetivo.id
        }
        comparacionActividades = obtenerComparacionActividades(programasOperativos,'d')
        comparacionActividades = json.dumps(comparacionActividades)
        return {
            'objetivo':objetivo,
            'tieneMetaCuantitativa':tieneMetaCuantitativa,
            'puntos':puntos,
            'numeroActividades':numeroActividades,
            'promedioGastoActividad':promedioGastoActividad,
            'promedioGastoBeneficairio':promedioGastoBeneficairio,
            'totalBeneficiarios':totalBeneficiarios,
            'promedioBeneficiariosActividad':promedioBeneficiariosActividad,
            'promedioInvolucradosActividad':promedioInvolucradosActividad,
            'porcentajeObjetivo':porcentajeObjetivo,
            'enteroPorcentajeObjetivo':enteroPorcentajeObjetivo,
            'claseSemaforo':claseSemaforo,
            'porcentajesProgramasOperativos':porcentajesProgramasOperativos,#nota: este reemplazó a 'metas'
            'comparacionActividades':comparacionActividades,
            'tablaCalorMesesActividades':tablaCalorMesesActividades,
            'tablaCalorDependencias': tablaCalorDependencias,
            'tablaCalorMeses':tablaCalorMeses,
            'gasto':gasto
        }
    def obtenerPorcentajeEje(self,idEje):
        """sujeto a cambio cuando los ejes se hagan modelos"""
        opcionesEjesTransversales = {
            '1':'Desarrollo Integral',
            '2':'Desarrollo Social y Humano',
            '3':'Promoción Económica y Medio Ambiente',
            '4':'Seguridad Ciudadana y Protección Civil',
            '5':'Combate a la Corrupción y Participación Ciudadana'
        }
        meses = obtenerMesesGobierno()
        objetivos = Objetivo.objects.filter(ejeTransversal=idEje)
        programasOperativos__acciones = ProgramaOperativo.acciones.through.objects.filter(acciones__objetivo__ejeTransversal=idEje)
        programasOperativos = []
        dependencias = []
        for po_accion in programasOperativos__acciones:
            programaOperativo = ProgramaOperativo.objects.get(pk=po_accion.programaoperativo_id)
            programasOperativos.append(programaOperativo)
            dependencias.append(programaOperativo.dependencia)
        dependencias = list(set(dependencias))
        programasOperativos = list(set(programasOperativos))
        #Aquí ttsbsjamos con la tabla de calor
        tablaCalorMesesActividades = obtenerComparacionActividadesMeses(programasOperativos,'d',dependencias,meses)
        tablaCalorMesesActividades = json.dumps(tablaCalorMesesActividades)
        tablaCalorDependencias = []
        for dependencia in dependencias:
            tablaCalorDependencias.append(dependencia.nombre)
        tablaCalorDependencias = json.dumps(tablaCalorDependencias)
        tablaCalorMeses = json.dumps(meses)
        #********************************************
        puntos = []
        porcentajesProgramasOperativos = []
        numeroActividades = 0
        gasto = 0
        totalBeneficiarios = 0
        totalInvolucrados = 0
        promedioBeneficiariosActividad = 0
        acumuladorPorcentajesDependencias = 0
        porcentajeProgramaOperativo = 0
        promedioInvolucradosActividad = 0
        promedioGastoActividad = 0
        porcentajeEje = 0
        for programaOperativo in programasOperativos:
            porcentajeProgramaOperativo= self.obtenerPorcentajeProgramaOperativo(programaOperativo.id)
            porcentajeEje = 100 if porcentajeProgramaOperativo['tieneMetaCuantitativa'] == False else 0
            tieneMetaCuantitativa = True if porcentajeProgramaOperativo['tieneMetaCuantitativa'] else False
            acumuladorPorcentajesDependencias += porcentajeProgramaOperativo['porcentajePo']
            puntos.extend(json.loads(porcentajeProgramaOperativo['puntos']))
            numeroActividades += porcentajeProgramaOperativo['numeroActividades']
            gasto += porcentajeProgramaOperativo['gasto']
            totalBeneficiarios += porcentajeProgramaOperativo['totalBeneficiarios']
            totalInvolucrados += porcentajeProgramaOperativo['totalInvolucrados']
            porcentajesProgramasOperativos.append(porcentajeProgramaOperativo)
        gasto = round(gasto,2)
        porcentajeEje = round(acumuladorPorcentajesDependencias / len(porcentajesProgramasOperativos),2) if len(porcentajesProgramasOperativos) > 0 else 0
        enteroPorcentajeEje = int(porcentajeEje)
        promedioGastoBeneficairio = round(gasto / totalBeneficiarios,2) if totalBeneficiarios >0 else 0
        if numeroActividades >0:
            promedioBeneficiariosActividad = int(totalBeneficiarios / numeroActividades) 
            promedioInvolucradosActividad = int(totalInvolucrados / numeroActividades)
            promedioGastoActividad = round(gasto / numeroActividades,2)
        claseSemaforo = 'danger'
        if porcentajeEje > 34 and porcentajeEje < 85:
            claseSemaforo = 'warning'
        elif porcentajeEje >= 85:
            claseSemaforo = 'success'
        puntos = json.dumps(puntos)
        porcentajesProgramasOperativos = json.dumps(porcentajesProgramasOperativos)
        eje ={
            'nombre':opcionesEjesTransversales[idEje],
            'id':idEje
        }
        comparacionActividades = obtenerComparacionActividades(programasOperativos,'d')
        comparacionActividades = json.dumps(comparacionActividades)
        print(eje)
        return {
            'eje':eje,
            'tieneMetaCuantitativa':tieneMetaCuantitativa,
            'puntos':puntos,
            'numeroActividades':numeroActividades,
            'promedioGastoActividad':promedioGastoActividad,
            'promedioGastoBeneficairio':promedioGastoBeneficairio,
            'totalBeneficiarios':totalBeneficiarios,
            'promedioBeneficiariosActividad':promedioBeneficiariosActividad,
            'promedioInvolucradosActividad':promedioInvolucradosActividad,
            'porcentajeEje':porcentajeEje,
            'enteroPorcentajeEje':enteroPorcentajeEje,
            'claseSemaforo':claseSemaforo,
            'porcentajesProgramasOperativos':porcentajesProgramasOperativos,#nota: este reemplazó a 'metas'
            'comparacionActividades':comparacionActividades,
            'tablaCalorMesesActividades':tablaCalorMesesActividades,
            'tablaCalorDependencias': tablaCalorDependencias,
            'tablaCalorMeses':tablaCalorMeses,
            'gasto':gasto
        }
    def obtenerPorcentajePMD(self):
        return ''

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
        contexto = PorcentajesMetas.obtenerPorcentajeAccion(self,idAccion=idAccion)
        return render(request,'indicadores/fichaAccion.html',contexto)

class FichaProgramaOperativo(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idPrograma):
        porcentajeMetas = PorcentajesMetas()
        contexto = porcentajeMetas.obtenerPorcentajeProgramaOperativo(idPrograma)
        return render(request,'indicadores/fichaProgramaOperativo.html',contexto)

class FichaDependencia(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idDependencia):
        porcentajeMeta = PorcentajesMetas()
        contexto = porcentajeMeta.obtenerPorcentajeDependencia(idDependencia)
        return render(request,'indicadores/fichaDependencia.html',contexto)

class FichaObjetivo(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idObjetivo):
        porcentajeMeta = PorcentajesMetas()
        contexto = porcentajeMeta.obtenerPorcentajeObjetivo(idObjetivo)
        return render(request,'indicadores/fichaObjetivo.html',contexto)

class FichaEje(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idEje):
        porcentajeMeta = PorcentajesMetas()
        contexto = porcentajeMeta.obtenerPorcentajeEje(idEje)
        return render(request,'indicadores/fichaEje.html',contexto)

class FichasAdmin(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        opcionesEjesTransversales = {
            '1':'Desarrollo Integral',
            '2':'Desarrollo Social y Humano',
            '3':'Promoción Económica y Medio Ambiente',
            '4':'Seguridad Ciudadana y Protección Civil',
            '5':'Combate a la Corrupción y Participación Ciudadana'
        }
        #TO:DO quitar cuando se haga genérico
        #TO:DO definir cabeceras base y hacerlo dinámico, dependendiendo de lo que elija
        programasOperativos = ProgramaOperativo.objects.filter(estado='a')
        acciones_po = []
        for programaOperativo in programasOperativos:
            accionesPo = programaOperativo.acciones.all()
            for accion in accionesPo:
                idEje = accion.objetivo.ejeTransversal
                eje = {
                    'id':idEje,
                    'nombre':opcionesEjesTransversales[idEje]
                }
                acciones_po.append({
                    'accion':accion,
                    'programaOperativo':programaOperativo,
                    'eje':eje
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
