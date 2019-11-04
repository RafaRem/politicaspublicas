from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.core import serializers
from django.contrib import messages
"""Models"""
from apps.programaOperativo.models import ProgramaOperativo,GastoAnualAsignado,Acciones,DetallesGasto
from apps.dependencia.models import Departamento,Dependencia
from apps.indicador.models import PeriodoGobierno,Periodo, Configuracion

def getGastoPeriodo(accion,periodo):
    gastos = DetallesGasto.objects.filter(accion=accion,periodo=periodo)
    total = 0.0
    for gasto in gastos:
        total += float(gasto.cantidad)
    return round(total,2) 

def getAccionesDependencia(dependencia,periodos):
    acciones = []
    programasOperativos = ProgramaOperativo.objects.filter(dependencia=dependencia, estado='a')
    for programaOperativo in programasOperativos:
        accionesPo = programaOperativo.acciones.all()
        for accion in accionesPo:
            gastos = DetallesGasto.objects.filter(accion=accion)
            periodosDetalleGasto = []
            for periodo in periodos:
                periodosDetalleGasto.append({
                    'gasto':getGastoPeriodo(accion,periodo),
                    'periodo':periodo
                })
            acciones.append({
                'accion':accion,
                'programaOperativo':programaOperativo,
                'periodos':periodosDetalleGasto
            })
    return acciones

# Create your views here.
class ProgramasOperativosList(LoginRequiredMixin,View):
    """Will show all the department's operative programs"""
    login_url = 'login'
    def get_context(self,request):
        programasOperativos = ProgramaOperativo.objects.filter(estado='a',dependencia=request.user.profile.dependencia)
        programasOperativos = programasOperativos.order_by('nombre')
        departamentos = Departamento.objects.filter(dependencia=request.user.profile.dependencia)
        departamentos = departamentos.order_by('nombre')
        departamentos = serializers.serialize('json',departamentos)
        faltaPorAsignar = False
        for programaOperativo in programasOperativos:
            if not programaOperativo.departamento:
                faltaPorAsignar = True
                break
        return {
            'programasOperativos':programasOperativos,
            'departamentos':departamentos,
            'tieneDepartamentos':request.user.profile.dependencia.tieneDepartamentos,
            'faltaPorAsignar':faltaPorAsignar
        }
    def get(self,request):
        return render(request,'dependencias/programasoperativos.html',self.get_context(request))
    def post(self,request):
        #values comes separated by | where the first element is the operative program and the second is the department 
        valoresPo_Dep = request.POST.getlist('valoresDependencia')
        for valorPo_Dep in valoresPo_Dep:
            #0 value is the operative program's id and 1 is the department's id
            arrValor = valorPo_Dep.split('|')
            programaOperativo = ProgramaOperativo.objects.get(pk=arrValor[0])
            departamento = Departamento.objects.get(pk=arrValor[1])
            programaOperativo.departamento = departamento
            programaOperativo.save()
            pass
        messages.success(request,'Departamentos cambiados con éxito')
        return render(request,'dependencias/programasoperativos.html',self.get_context(request))        
    
class PresupuestoAnualList(LoginRequiredMixin,View):
    login_url = 'login'
    def obtenerContexto(self,idProgramaOperativo):
        programaOperativo = ProgramaOperativo.objects.get(pk=idProgramaOperativo)
        configuracion = Configuracion.objects.get(pk=1)
        periodo = configuracion.periodoGobierno
        presupuestosPeriodo = []
        #se hará de la siguiente manera para hacer un if en el template 
        #en caso de que no haya sido asignado
        faltaAsignar = False
        try:
            gastoAnualAsignado = GastoAnualAsignado.objects.get(
            programaOperativo=programaOperativo,
            periodoGobierno=periodo)
        except:
            #Si no existe, esta variable será necesaria para poder asignar
            faltaAsignar = True
            gastoAnualAsignado = {
                'permitirModificar':True
            }

        presupuestosPeriodo.append({
            'periodo':periodo,
            'presupuesto':gastoAnualAsignado
        })
        return {
            'presupuestosPeriodo':presupuestosPeriodo,
            'programaOperativo':programaOperativo,
            'faltaAsignar':faltaAsignar
        }
    def get(self,request,idProgramaOperativo):
        contexto = self.obtenerContexto(idProgramaOperativo)
        return render(request,'dependencias/presupuestoAnual.html',contexto)
    def post(self,request,idProgramaOperativo):
        valoresPresupuesto = request.POST.getlist('valoresPresupuesto')
        for valorPresupuesto in valoresPresupuesto:
            #la posición 0 es el id del periodo, la 1 es la cantidad
            valores = valorPresupuesto.split('|')
            programaOperativo = ProgramaOperativo.objects.get(pk=idProgramaOperativo)
            periodo = PeriodoGobierno.objects.get(pk=valores[0])
            try:
                gastoAnual = GastoAnualAsignado.objects.get(
                programaOperativo=programaOperativo,
                periodoGobierno=periodo
                )
                gastoAnual.programaOperativo = programaOperativo
                gastoAnual.cantidad = valores[1]
                gastoAnual.periodoGobierno = periodo
                gastoAnual.permitirModificar = False
            except :
                gastoAnual = GastoAnualAsignado.objects.create(
                programaOperativo=programaOperativo,
                cantidad=valores[1],
                periodoGobierno=periodo,
                permitirModificar=False
                )
            messages.success(request,'Programa presupuestado para el periodo '+periodo.descripcion+
            '. Si se desea modificar, ponerse en contacto con la Dirección de Planeación e Innovación Gubernamental')
        
            gastoAnual.save()
        contexto = self.obtenerContexto(idProgramaOperativo)
        return render(request,'dependencias/presupuestoAnual.html',contexto)

class AccionesDependencia(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,idDependencia):
        dependencia = Dependencia.objects.get(pk=idDependencia)
        if request.user.profile.tipoUsuario == 'e' and str(request.user.profile.dependencia.id) != idDependencia:
            return redirect('index')            
        periodos = Periodo.objects.filter(capturaHabilitada=True)
        acciones_po = getAccionesDependencia(dependencia,periodos)
        return render(request,'dependencias/acciones.html',{
            'acciones_po':acciones_po,
            'periodos':periodos,
            'dependencia':dependencia
        })

class DependenciasAdmin(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        if (request.user.profile.tipoUsuario != 'a') and (request.user.profile.tipoUsuario != 's'):
            return redirect('index')
        periodos = Periodo.objects.all() #[30,30,30]
        dependencias = Dependencia.objects.filter(estado='a')
        dpendencias_periodosGasto = []
        for dependencia in dependencias:
            acciones_po = getAccionesDependencia(dependencia,periodos)
            totalGastoDependencia = [0.0] * len(periodos)
            for accion_po in acciones_po:
                for i in range(0,len(periodos)):
                    totalGastoDependencia[i] += float(accion_po['periodos'][i]['gasto'])
                    totalGastoDependencia[i] = round(totalGastoDependencia[i],2)
            dpendencias_periodosGasto.append({
                'dependencia':dependencia,
                'gastos':totalGastoDependencia
            })
        return render(request,'dependencias/admin/Dependencias.html',{
              'periodos':periodos,
              'dpendencias_periodosGasto':dpendencias_periodosGasto
        })
