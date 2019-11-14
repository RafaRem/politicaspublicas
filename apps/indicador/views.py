import json
import random
from django.core import serializers
from datetime import datetime, timedelta
from collections import OrderedDict
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q,Count
"""funciones de otras vistas"""
from apps.dependencia.views import getGastoPeriodoAccion
from apps.programaOperativo.views import ListActividadesAdmin
"""Modelos"""
from apps.indicador.models import PeriodoGobierno, Meta, Configuracion, Periodo
from apps.programaOperativo.models import Acciones,ProgramaOperativo,Actividad,Variable,DetallesGasto, MetaAccion
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
    configuracion = Configuracion.objects.get(pk=1)
    consulta &= Q(fecha_fi__range=(configuracion.periodoGobierno.fechaInicial,configuracion.periodoGobierno.fechaFinal))
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

def obtenerComparacionActividadesMeses(arreglo,filtrarPor,xAxis,yAxis,valorFiltro):
    """Opciones: 'e' = dependencias, 'o' = objetivo.
     programasOperativos es un arreglo de programas operativos a comparar.
     filtrarPor será el filtro"""
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
            if filtrarPor =='e':
                actividades = Actividad.objects.filter(programaoperativo__dependencia=valx,
                fecha_fi__gte=fechaDesde,fecha_fi__lte=fechaHasta, 
                accion__objetivo__ejeTransversal=valorFiltro)
                resultado.append([x,y,actividades.count()])       
            if filtrarPor =='o':
                objetivo = Objetivo.objects.get(pk=valorFiltro)
                actividades = Actividad.objects.filter(programaoperativo__dependencia=valx,
                fecha_fi__gte=fechaDesde,fecha_fi__lte=fechaHasta, 
                accion__objetivo=objetivo)
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

def obtenerCantidadesBrutasMetas(tipoArreglo, arreglo):
    """El tipo de arreglo si es 'p' es programa operativo"""
    metas = []
    if tipoArreglo == 'p':
        for programaOperativo in arreglo:
            porcentajesAcciones = json.loads(programaOperativo['porcentajesAcciones'])
            for porcentajeAccion in porcentajesAcciones:
                meta = porcentajeAccion['meta']
                accion = porcentajeAccion['accion']['nombre']
                if meta['tieneMeta']:
                    metas.append({
                        'accion':accion,
                        'id':porcentajeAccion['accion']['id'],
                        'descripcion':meta['descripcionMeta'],
                        'cantidad':meta['cantidadMeta']
                    })
    return metas

class PorcentajesMetas():
    """ESTE ES VIEJOOOOOO NO SIRVEEEEEEEEEEEEE PARA LA NUEVA VERSIÓN"""
    def obtenerActividadesGastos(self,tipo,arreglo):
        """si tipo es 'o' se hará por objetivos en el xAxis"""
        if tipo == 'o':
            #el arreglo son los programas operativos
            gastos = []
            objetivo_id = []
            descripcionesObjetivo = []
            totalActividades = []
            for programaOperativo in arreglo:
                porcentajesAcciones = json.loads(programaOperativo['porcentajesAcciones'])
                for porcentajeAccion in porcentajesAcciones:
                    objetivoIndex = 0
                    # print(porcentajeAccion)
                    if porcentajeAccion['accion']['objetivo_id'] in objetivo_id:
                        objetivoIndex = objetivo_id.index(porcentajeAccion['accion']['objetivo_id'])
                    else:
                        objetivo_id.append(porcentajeAccion['accion']['objetivo_id'])
                        descripcionesObjetivo.append(porcentajeAccion['accion']['objetivo'])
                        gastos.append(0)
                        totalActividades.append(0)
                        objetivoIndex = len(objetivo_id) - 1
                    gastos[objetivoIndex] += float(porcentajeAccion['gasto'])
                    totalActividades[objetivoIndex] += int(porcentajeAccion['numeroActividades'])
            return{
                'gastos':gastos,
                'totalActividades':totalActividades,
                'descripcionesObjetivo':descripcionesObjetivo
            }
        return ''
    def obtenerPorcentajeAccion(self, idAccion):
        accion = Acciones.objects.get(pk=idAccion)
        configuracion = Configuracion.objects.get(pk=1)
        actividades = obtenerActividades(
            idAccion=int(idAccion)
        )
        numeroActividades = 0
        numeroActividadesSecundarias = 0
        #los puntos son de geolicalización
        puntos = obtenerGeoPuntosActividades(actividades)
        puntos = json.dumps(puntos)
        periodosGasto = Periodo.objects.filter(fechaFinal__range=(configuracion.periodoGobierno.fechaInicial,configuracion.periodoGobierno.fechaFinal))
        gasto = 0
        for periodoGasto in periodosGasto:
            gasto += getGastoPeriodoAccion(accion,periodoGasto)
        gasto = round(gasto,2)
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
        if accion.meta.filter(periodo=configuracion.periodoGobierno).first():
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
            numeroActividades += resultadoAccion['contadorActividades']
        else:
            claseSemaforo = 'info'
            meta = {
                'tieneMeta':False,
                'porcentajeMeta':100,
                'claseSemaforo':claseSemaforo,
                'descripcionMeta':'meta cualitativa',
                'cantidadMeta':''
            }
        for actividad in actividades:
            if actividad.estado == 's':
                numeroActividadesSecundarias += actividad.multiplicador
        numeroActividades = numeroActividades + numeroActividadesSecundarias
        accion = {
            'id':accion.id,
            'nombre':accion.nombre,
            'objetivo_id':accion.objetivo.id,
            'objetivo':accion.objetivo.nombre,
            'ejeTransversal_id':accion.objetivo.ejeTransversal
        }
        return {
            'accion':accion,
            'puntos':puntos,
            'numeroActividades':numeroActividades,
            'numeroActividadesSecundarias':numeroActividadesSecundarias,
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
        numeroActividadesSecundarias = 0
        gasto = 0
        totalBeneficiarios = 0
        totalInvolucrados = 0
        promedioBeneficiariosActividad = 0
        promedioInvolucradosActividad = 0
        porcentajePo = 0
        acumuladorPorcentajeAcciones = 0
        promedioGastoActividad = 0
        tieneMetaCuantitativa = False
        contadorAccionesCuantitativas = 0
        for accion in acciones:
            porcentajePo = 100 if accion.cualitativa == True else 0
            porcentajeAccion = self.obtenerPorcentajeAccion(accion.id)
            puntos.extend(json.loads(porcentajeAccion['puntos']))
            numeroActividades += porcentajeAccion['numeroActividades']
            numeroActividadesSecundarias += porcentajeAccion['numeroActividadesSecundarias']
            gasto += porcentajeAccion['gasto']
            totalBeneficiarios += porcentajeAccion['totalBeneficiarios']
            totalInvolucrados += porcentajeAccion['totalInvolucrados']
            if porcentajeAccion['meta']['claseSemaforo'] != 'info':
                tieneMetaCuantitativa = True
                contadorAccionesCuantitativas += 1
                acumuladorPorcentajeAcciones += porcentajeAccion['meta']['porcentajeMeta']
            porcentajesAcciones.append(porcentajeAccion)
        porcentajePo = round(acumuladorPorcentajeAcciones / contadorAccionesCuantitativas,2) if contadorAccionesCuantitativas > 0 else 0
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
            'numeroActividadesSecundarias':numeroActividadesSecundarias,
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
        programasOperativos = ProgramaOperativo.objects.filter(dependencia=dependencia, estado='a')
        puntos = []
        porcentajesProgramasOperativos = []
        numeroActividades = 0
        numeroActividadesSecundarias = 0
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
        contadorPosCuantitativos = 0
        for programaOperativo in programasOperativos:
            porcentajeProgramaOperativo= self.obtenerPorcentajeProgramaOperativo(programaOperativo.id)
            if porcentajeProgramaOperativo['tieneMetaCuantitativa'] == True:
                tieneMetaCuantitativa = True
                acumuladorPorcentajesPos += porcentajeProgramaOperativo['porcentajePo']
                contadorPosCuantitativos += 1
            porcentajeDireccion = 100 if porcentajeProgramaOperativo['tieneMetaCuantitativa'] == False else 0
            puntos.extend(json.loads(porcentajeProgramaOperativo['puntos']))
            numeroActividades += porcentajeProgramaOperativo['numeroActividades']
            numeroActividadesSecundarias += porcentajeProgramaOperativo['numeroActividadesSecundarias']
            gasto += porcentajeProgramaOperativo['gasto']
            totalBeneficiarios += porcentajeProgramaOperativo['totalBeneficiarios']
            totalInvolucrados += porcentajeProgramaOperativo['totalInvolucrados']
            porcentajesProgramasOperativos.append(porcentajeProgramaOperativo)
        cantidadesBrutasMetas = obtenerCantidadesBrutasMetas('p',porcentajesProgramasOperativos)
        porcentajeDireccion = round(acumuladorPorcentajesPos / contadorPosCuantitativos,2) if contadorPosCuantitativos > 0 else 0
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
            'numeroActividadesSecundarias':numeroActividadesSecundarias,
            'promedioGastoActividad':promedioGastoActividad,
            'promedioGastoBeneficairio':promedioGastoBeneficairio,
            'totalBeneficiarios':totalBeneficiarios,
            'totalInvolucrados':totalInvolucrados,
            'promedioBeneficiariosActividad':promedioBeneficiariosActividad,
            'promedioInvolucradosActividad':promedioInvolucradosActividad,
            'porcentajeDireccion':porcentajeDireccion,
            'enteroPorcentajeDireccion':enteroPorcentajeDireccion,
            'claseSemaforo':claseSemaforo,
            'cantidadesBrutasMetas':cantidadesBrutasMetas,
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
        tablaCalorMesesActividades = obtenerComparacionActividadesMeses(programasOperativos,'o',dependencias,meses,idObjetivo)
        tablaCalorMesesActividades = json.dumps(tablaCalorMesesActividades)
        tablaCalorDependencias = []
        for dependencia in dependencias:
            tablaCalorDependencias.append(dependencia.nombre)
        tablaCalorDependencias = json.dumps(tablaCalorDependencias)
        tablaCalorMeses = json.dumps(meses)
        puntos = []
        porcentajesProgramasOperativos = []
        numeroActividades = 0
        numeroActividadesSecundarias = 0
        gasto = 0
        totalBeneficiarios = 0
        totalInvolucrados = 0
        promedioBeneficiariosActividad = 0
        acumuladorPorcentajesDependencias = 0
        porcentajeProgramaOperativo = 0
        promedioInvolucradosActividad = 0
        promedioGastoActividad = 0
        porcentajeObjetivo = 0
        contadorPosCuantitativos = 0
        for programaOperativo in programasOperativos:
            porcentajeProgramaOperativo= self.obtenerPorcentajeProgramaOperativo(programaOperativo.id)
            porcentajeObjetivo = 100 if porcentajeProgramaOperativo['tieneMetaCuantitativa'] == False else 0
            if porcentajeProgramaOperativo['tieneMetaCuantitativa']:
                acumuladorPorcentajesDependencias += porcentajeProgramaOperativo['porcentajePo']
                contadorPosCuantitativos += 1   
            tieneMetaCuantitativa = True if porcentajeProgramaOperativo['tieneMetaCuantitativa'] else False
            puntos.extend(json.loads(porcentajeProgramaOperativo['puntos']))
            numeroActividades += porcentajeProgramaOperativo['numeroActividades']
            numeroActividadesSecundarias += porcentajeProgramaOperativo['numeroActividadesSecundarias']
            gasto += porcentajeProgramaOperativo['gasto']
            totalBeneficiarios += porcentajeProgramaOperativo['totalBeneficiarios']
            totalInvolucrados += porcentajeProgramaOperativo['totalInvolucrados']
            porcentajesProgramasOperativos.append(porcentajeProgramaOperativo)
        gasto = round(gasto,2)
        porcentajeObjetivo = round(acumuladorPorcentajesDependencias / contadorPosCuantitativos,2) if contadorPosCuantitativos > 0 else 0
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
            'numeroActividadesSecundarias':numeroActividadesSecundarias,
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
        tablaCalorMesesActividades = obtenerComparacionActividadesMeses(programasOperativos,'e',dependencias,meses,idEje)
        tablaCalorMesesActividades = json.dumps(tablaCalorMesesActividades)
        tablaCalorDependencias = []
        for dependencia in dependencias:
            tablaCalorDependencias.append(dependencia.nombre)
        tablaCalorDependencias = json.dumps(tablaCalorDependencias)
        tablaCalorMeses = json.dumps(meses)
        #*********************************************
        puntos = []
        porcentajesProgramasOperativos = []
        numeroActividades = 0
        numeroActividadesSecundarias = 0
        gasto = 0
        totalBeneficiarios = 0
        totalInvolucrados = 0
        promedioBeneficiariosActividad = 0
        acumuladorPorcentajesDependencias = 0
        porcentajeProgramaOperativo = 0
        promedioInvolucradosActividad = 0
        promedioGastoActividad = 0
        porcentajeEje = 0
        contadorPosCuantitativos = 0
        for programaOperativo in programasOperativos:
            porcentajeProgramaOperativo= self.obtenerPorcentajeProgramaOperativo(programaOperativo.id)
            porcentajeEje = 100 if porcentajeProgramaOperativo['tieneMetaCuantitativa'] == False else 0
            tieneMetaCuantitativa = True if porcentajeProgramaOperativo['tieneMetaCuantitativa'] else False
            if porcentajeProgramaOperativo['tieneMetaCuantitativa']:
                acumuladorPorcentajesDependencias += porcentajeProgramaOperativo['porcentajePo']
                contadorPosCuantitativos += 1
            puntos.extend(json.loads(porcentajeProgramaOperativo['puntos']))
            numeroActividades += porcentajeProgramaOperativo['numeroActividades']
            gasto += porcentajeProgramaOperativo['gasto']
            totalBeneficiarios += porcentajeProgramaOperativo['totalBeneficiarios']
            totalInvolucrados += porcentajeProgramaOperativo['totalInvolucrados']
            porcentajesProgramasOperativos.append(porcentajeProgramaOperativo)
        gasto = round(gasto,2)
        porcentajeEje = round(acumuladorPorcentajesDependencias / contadorPosCuantitativos,2) if contadorPosCuantitativos > 0 else 0
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
        
        graficaActividadesGastos = self.obtenerActividadesGastos(tipo='o',arreglo=porcentajesProgramasOperativos)
        graficaActividadesGastos = json.dumps(graficaActividadesGastos)
        puntos = json.dumps(puntos)
        porcentajesProgramasOperativos = json.dumps(porcentajesProgramasOperativos)

        eje ={
            'nombre':opcionesEjesTransversales[idEje],
            'id':idEje
        }
        comparacionActividades = obtenerComparacionActividades(programasOperativos,'d')
        comparacionActividades = json.dumps(comparacionActividades)
        return {
            'eje':eje,
            'tieneMetaCuantitativa':tieneMetaCuantitativa,
            'puntos':puntos,
            'numeroActividades':numeroActividades,
            'numeroActividadesSecundarias':numeroActividadesSecundarias,
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
            'graficaActividadesGastos':graficaActividadesGastos,
            'gasto':gasto
        }
    def obtenerPorcentajePMD(self):
        return ''

class EstadísticosMetas():
    """Nueva versión"""
    def obtenerSemaforo(self,cantidad,tieneMeta=False):
        'obtiene la clase de semáforo que se utilizará'
        if not tieneMeta:
            return 'info'
        if cantidad <= 40:
            return 'danger'
        elif cantidad > 40 and cantidad <= 80:
            return 'warning'
        else:
            return 'success'
    def obtenerEstadisticoAccion(self,idAccion):
        accion = Acciones.objects.get(pk=idAccion)
        metasAccion = MetaAccion.objects.filter(accion=accion)
        #Este arreglo guarda los resultados de las metas
        if metasAccion:
            tieneMeta = True
        #*********Metas
        resultadosMetas = []
        porcentajeAvancePonderadoDecimal = 0
        sumaPorcentajeAvancePonderado = 0
        variablesActividad = VariableActividad.objects.filter(
            variable=metaAccion.variable)
        for metaAccion in metasAccion:
            variablesActividadAccion = variablesActividad.filter(
                actividad__accion=accion,
                variable=metaAccion.variable)
            sumaVariable = sum(int(c.cantidad) for c in variablesActividadAccion)
            resultadoDecimal = round(((sumaVariable / metaAccion) * 100),2)
            sumaPorcentajeAvancePonderado += resultadoDecimal
            resultadoEntero=int(round(resultadoDecimal,0))
            resultadosMetas.append({
                'idVariable':metaAccion.variable.id,
                'nombreVariable':metaAccion.variable.nombre,
                'cantidadRealizada':sumaVariable,
                'cantidadMeta':metaAccion.cantidad,
                'resultadoDecimal':resultadoDecimal,
                'resultadoEntero':resultadoEntero,
                'claseSemaforo':self.obtenerSemaforo(cantidad=resultadoDecimal,tieneMeta=True)
            })
        porcentajeAvancePonderadoDecimal = round((sumaPorcentajeAvancePonderado / metaAccion.count()) * 100,2)
        porcentajeAvancePonderadoEntero = int(round(porcentajeAvancePonderadoDecimal,0))
        #****Metas
        return {
            'idAccion':accion.id,
            'nombreAccion':accion.nombre,
            'resultadosMetas':resultadosMetas,
            'porcentajeAvancePonderadoDecimal':porcentajeAvancePonderadoDecimal,
            'porcentajeAvancePonderadoEntero':porcentajeAvancePonderadoEntero
            'variablesActividad':variablesActividad,
            'tieneMeta':tieneMeta
        }

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
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's') and (request.user.profile.tipoUsuario != 'i'):
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
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's') and (request.user.profile.tipoUsuario != 'i'):
            return redirect('index')
        accion = Acciones.objects.get(pk=idAccion)
        contexto = self.getContexto(accion)
        return render(request,'indicadores/metas/capturarMetasForm.html',contexto)
    def post(self,request,idAccion):
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's') and (request.user.profile.tipoUsuario != 'i'):
            return redirect('index')
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
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's') and (request.user.profile.tipoUsuario != 'i'):
            return redirect('index')
        contexto = PorcentajesMetas.obtenerPorcentajeAccion(self,idAccion=idAccion)
        return render(request,'indicadores/fichaAccion.html',contexto)

class FichaProgramaOperativo(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idPrograma):
        programaOperativo = ProgramaOperativo.objects.get(pk=idPrograma)
        if (str(request.user.profile.dependencia.id) != str(programaOperativo.dependencia.id)) and ((request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's') and (request.user.profile.tipoUsuario != 'i')):
            return redirect('index')
        porcentajeMetas = PorcentajesMetas()
        contexto = porcentajeMetas.obtenerPorcentajeProgramaOperativo(idPrograma)
        return render(request,'indicadores/fichaProgramaOperativo.html',contexto)

class FichaDependencia(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idDependencia):
        if (str(request.user.profile.dependencia.id) != str(idDependencia)) and ((request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's') and (request.user.profile.tipoUsuario != 'i')):
            return redirect('index')
        porcentajeMeta = PorcentajesMetas()
        contexto = porcentajeMeta.obtenerPorcentajeDependencia(idDependencia)
        return render(request,'indicadores/fichaDependencia.html',contexto)
    def post(self,request, idDependencia):
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

class FichaObjetivo(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idObjetivo):
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's') and (request.user.profile.tipoUsuario != 'i'):
            return redirect('index')
        porcentajeMeta = PorcentajesMetas()
        contexto = porcentajeMeta.obtenerPorcentajeObjetivo(idObjetivo)
        return render(request,'indicadores/fichaObjetivo.html',contexto)

class FichaEje(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, idEje):
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's') and (request.user.profile.tipoUsuario != 'i'):
            return redirect('index')
        porcentajeMeta = PorcentajesMetas()
        contexto = porcentajeMeta.obtenerPorcentajeEje(idEje)
        return render(request,'indicadores/fichaEje.html',contexto)

class FichasAdmin(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's') and (request.user.profile.tipoUsuario != 'i'):
            return redirect('index')
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
    def reconfigurarGastos(self):
        programasOperativos = ProgramaOperativo.objects.all()
        for po in programasOperativos:
            acciones = po.acciones.all()
            gastos = []
            periodos = []
            cantidades = []            
            for accion in acciones:
                detallesGasto = DetallesGasto.objects.filter(accion=accion)
                for detalleGasto in detallesGasto:
                    if (detalleGasto.gasto in gastos) and (detalleGasto.periodo in periodos):
                        try:
                            index = gastos.index(detalleGasto.gasto)
                        except expression as identifier:
                            import pdb; pdb.set_trace()
                            pass
                        cantidades[index] =float(cantidades[index]) + float(detalleGasto.cantidad)
                    else:
                        gastos.append(detalleGasto.gasto)
                        periodos.append(detalleGasto.periodo)
                        cantidades.append(detalleGasto.cantidad)
                    pass
                pass
            for i,gasto in enumerate(gastos):
                DetallesGasto.objects.create(
                    programaOperativo=po,
                    gasto=gastos[i],
                    cantidad=cantidades[i],
                    periodo=periodos[i]
                )
            
            pass
        detallesGasto = DetallesGasto.objects.filter(programaOperativo=None)
        detallesGasto.delete()
        return 0
    def get(self,request):
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's'):
            return redirect('index')
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
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's'):
            return redirect('index')
        configuracion = Configuracion.objects.get(pk=1)
        form = ConfiguracionesForm(request.POST,instance=configuracion)
        if form.is_valid(): 
            form.save()
        return render(request,'indicadores/configuraciones.html',{
            'form':form
        })

def generar_variables(request):
    metas = Meta.objects.all()
    for meta in metas:
        resultadoBusqueda = Variable.objects.filter(
            nombre__icontains=meta.descripcion
            )
        if not resultadoBusqueda:
            Variable.objects.create(
                nombre=meta.descripcion
                )
    return HttpResponse('ok')
