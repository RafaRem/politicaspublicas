from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
"""Modelos"""
from apps.indicador.models import PeriodoGobierno, Meta
from apps.programaOperativo.models import Acciones,ProgramaOperativo

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
  