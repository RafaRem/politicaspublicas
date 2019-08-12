from django.views.generic import TemplateView, View
from django.shortcuts import render
"""MOdelos"""
from apps.indicador.models import PeriodoGobierno, Meta
from apps.programaOperativo.models import Acciones

class RenderView(TemplateView):
    template_name = ".html"

class AccionesMetasView(View):
    def obtenerAcciones(self):
        acciones = Acciones.objects.all()
        #Aquí les va a decir si ya se capturó meta
    def get(self,request):
        periodos = PeriodoGobierno.objects.all()
        acciones = Acciones.objects.all()
        return render(request,'capturarMetas.html',{
            'periodos':periodos,
            'acciones':acciones
        })
class AccionesMetasForm(View):
    def getContexto(self,accion):
        periodos = PeriodoGobierno.objects.all()
        metas = accion.meta.all()
        return {
            'accion':accion,
            'periodos':periodos,
            'metas':metas
        }
    def get(self,request,idAccion):
        accion = Acciones.objects.get(pk=idAccion)
        contexto = self.getContexto(accion)
        return render(request,'capturarMetasForm.html',contexto)
    def post(self,request,idAccion):
        accion = Acciones.objects.get(pk=idAccion)
        contexto = self.getContexto(accion)
        periodos = PeriodoGobierno.objects.all()
        descripcionMeta = request.POST.get('descripcion')
        metasForm = request.POST.getlist('meta')
        metas = []
        for i in range(0,len(periodos)):
            meta = Meta.objects.create(descripcion=descripcionMeta,meta=metasForm[i],periodo=periodos[i])
            accion.meta.add(meta)
        return render(request,'capturarMetasForm.html',contexto)
