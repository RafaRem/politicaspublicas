from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import os
import json
"""MOdelos"""
from apps.indicador.models import PeriodoGobierno, Meta
from apps.programaOperativo.models import Acciones

class RenderView(TemplateView):
    template_name = ".html"

class ObtenerCoordenadas(View):
    def pruebaAPi(self,lugar):
        resp = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='+lugar+'&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key='+os.getenv('api_key'))
        resp.encoding = 'utf-8'
        return resp.json()
    def get(self,request):
        return render(request,'extras/generadorCoordenadas.html',{
            'jsonsLugares':'',
            'generados':False
        })
    def post(self,request):
        lugares = request.POST.getlist('lugares')
        jsonsLugares = []
        for lugar in lugares:
            jsonsLugares.append(self.pruebaAPi(lugar))
        jsonsLugares = json.dumps(jsonsLugares)
        return render(request,'extras/generadorCoordenadas.html',{
            'jsonsLugares':jsonsLugares,
            'generados':True
        })

    