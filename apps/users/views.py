from django.shortcuts import render
from . import forms
from django.views.generic import View
from .forms import RegistrarPersona
from .models import Persona
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.a
import time
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
# Create your views here.
def index(request):
    return render(request,'index.html')


class CalendarView(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'users/calendario.html', { })


def vista_registrar(request):
    if request.method=='POST':
        form = RegistrarPersona(request.POST)
        if form.is_valid():
            messages.success(request,"Registro con exito")
            form.save()
        return redirect("index")
    else:
        form = RegistrarPersona()
    return render(request,'users/RegistroPrueba.html',{'form': form})

class GraficaView(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'users/graficas.html', { })


class CharData(APIView):
    authentication_classes = []
    permission_classes =[]

    def get(self, request, format=None):
        nom = 10
        apepat = 18
        apemat = 7
        ed = 2
        #Var
        labels = ['Nombres', 'Apellidos P', 'Apellidos M', 'Edades']
        default_items = [nom,apepat,apemat,ed]
        title= 'Prueba'
        fecha= '2019-05-10'
        data ={
        "labels": labels,
        "default": default_items,
        "titulo": title,
        "fecha":fecha,
        }
        return Response(data)
