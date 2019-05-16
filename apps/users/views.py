#DJANGO classes
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.core import serializers
from django.contrib import messages
# decorators for login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#forms
from . import forms
from .forms import UsuariosForm
#Views
from django.views.generic import View
from .forms import RegistrarPersona
from rest_framework.views import APIView
#Models
from .models import Persona
# Create your views here.a
import time
import json
from rest_framework.response import Response


class IndexView(View):
    template_name = 'users/login.html'
    @method_decorator(login_required(login_url='login'))
    def get(self,request, *args, **kwargs):
        return render(request,'index.html')


class CalendarView(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'users/calendario.html', { })


class UsuarioView(View):
    def get(self, request):
        return render(request, 'index.html')



class LoginView(View):
    def post(self,request):
        username = str(request.POST['usuario']).lower()
        password = str(request.POST['pass'])
        if username:
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect(request.path) 
        print(request.POST['usuario'])
        return render(request,"users/login.html")
        pass
    def get(self,request):
        # print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return redirect('index')
        return render(request,"users/login.html")
        pass



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
