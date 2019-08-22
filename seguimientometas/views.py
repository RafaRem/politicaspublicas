from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import os
"""MOdelos"""
from apps.indicador.models import PeriodoGobierno, Meta
from apps.programaOperativo.models import Acciones

class RenderView(TemplateView):
    template_name = ".html"

class ObtenerCoordenadas(View):
    def pruebaAPi(self):
        resp = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=los mochis, sinaloa&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key='+os.getenv('api_key'))
        return resp
    def get(self,request):
        resp = self.pruebaAPi()
        return render(request,'extras/generadorCoordenadas.html')
    def post(self,request):
        lugares = request.POST.getlist('lugares')
        print(lugares)
        return render(request,'extras/generadorCoordenadas.html')

    