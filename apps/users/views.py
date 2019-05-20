#DJANGO classes
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
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
#Create your views here.a
import time
import json
from rest_framework.response import Response
from django.core import serializers

#Reporte
from django.utils import timezone
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table
from io import StringIO, BytesIO
import time

# Create your views here.

ejes = [
    {
        'numero':'Eje I',
        'nombre':'Desarrollo Integral',
        'clase':'eje1'
    },
    {
        'numero':'Eje II',
        'nombre':'Desarrollo Social y Humano',
        'clase':'eje2'
    },
    {
        'numero':'Eje III',
        'nombre':'Promoción Económica y Medio Ambiente',
        'clase':'eje3'
    },
    {
        'numero':'Eje IV',
        'nombre':'Seguridad Ciudadana y Protección Civil',
        'clase':'eje4'
    },
    {
        'numero':'Eje V',
        'nombre':'Combate a la Corrupción y Participación Ciudadana',
        'clase':'eje5'
    }
]


class IndexView(View):
    ejes = [
        {
            'numero':'Eje I',
            'nombre':'Desarrollo Integral',
            'clase':'eje1'
        },
        {
            'numero':'Eje II',
            'nombre':'Desarrollo Social y Humano',
            'clase':'eje2'
        },
        {
            'numero':'Eje III',
            'nombre':'Promoción Económica y Medio Ambiente',
            'clase':'eje3'
        },
        {
            'numero':'Eje IV',
            'nombre':'Seguridad Ciudadana y Protección Civil',
            'clase':'eje4'
        },
        {
            'numero':'Eje V',
            'nombre':'Combate a la Corrupción y Participación Ciudadana',
            'clase':'eje5'
        }
]
    template_name = 'users/login.html'
    @method_decorator(login_required(login_url='login'))
    def get(self,request, *args, **kwargs):
        print(self.ejes)
        return render(request,'index.html',{'ejes':self.ejes})


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
            if user != None:
                login(request,user)
                return redirect(request.path) 
            else:
                messages.error(request,'Usuario o contraseña inválidos')
                return redirect('login')
                
            
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def report(request):
    hour = timezone.localtime(timezone.now())
    formatedHour = hour.strftime("%H:%M:%S")
    formatedDay  = hour.strftime("%d/%m/%Y")
    time.sleep(1)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = Reporte.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    #Header
    c.setLineWidth(.3)
    c.drawImage("static/images/Ayuntamiento.jpg", 30, 750, width=70, height=70)
    c.drawImage("static/images/Ahome.png", 390, 750, width=170, height=60)
    c.drawImage("static/images/Marca.jpg", 65, 0, width=530, height=450)
    c.setFont('Helvetica',14)
    c.drawString(30,730,'Dirección de Planeación e Innovación Gubernamental')
    c.setFont('Helvetica',12)
    c.drawString(30,715,'Reporte de Evaluación')
    #c.setFont('Helvetica',12)

    c.setFont('Helvetica-Bold',12)
    c.drawString(440,730, formatedHour)
    c.line(420,727,520,727)
    c.drawString(440,715, formatedDay)
    c.line(40,70,500,70)
    c.setFont('Helvetica',8)
    c.drawString(40,55,'Degollado y Cuauhtémoc S/N, Colonia Bienestar, C.P. 81280, Los Mochis, Ahome, Sinaloa')
    c.drawString(40,45,'ahome.gob.mx   #Transformando Ahome ')
    
    # Header
         
    #TableHeader
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize=10
    # Table 
    # styleN = styles["BodyText"]
    # styleN.alignment = TA_CENTER
    # styleN.fontSize=7

    #pdf save
    c.showPage()
    c.save()
    pdf= buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response