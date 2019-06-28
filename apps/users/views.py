#DJANGO classes
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
# decorators for login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
#forms
from . import forms
from .forms import UsuariosForm
#Views
from django.views.generic import View
from .forms import RegistrarPersona
from rest_framework.views import APIView
#Models
from .models import Persona
from apps.dependencia.models import Dependencia
from apps.objetivo.models import Objetivo
from apps.programaOperativo.models import Actividad, ProgramaOperativo
from django.db.models import  *
from django.contrib.auth.models import User
#Create your views here.a
import time
import json
from rest_framework.response import Response
from django.core import serializers
from datetime import datetime
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


class IndexView(LoginRequiredMixin,View):
    login_url = 'login'
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
    def get(self,request, *args, **kwargs):
        return render(request,'index.html',{'ejes':self.ejes})

@login_required(login_url='login')
def CalendarView(request):
    #Model.objects.filter(fecha__range=(f_inicial, f_cierre) CONSULTA POR RANGO DE FECHAS
    hour = timezone.localtime(timezone.now())
    formatedDay  = hour.strftime("%Y/%m/%d")
    date_object = datetime.strptime(formatedDay, '%Y/%m/%d')
    matchs = Actividad.objects.all()
    depend = Dependencia.objects.all()
    objetivo = Objetivo.objects.all()
    colores=[]
    for i in matchs:
        if (date_object.date() > i.fecha_in):
            colores+= ['red']
        else:
            colores+= ['green']

    evento =zip(matchs, colores)
    contador = matchs.count()

    #   GENERAL ************************************************
    if request.method== 'POST':
        srch = request.POST['srh']
        srch2 = request.POST['srh2']
        srch3 = request.POST['srh3']
        srch4 = request.POST['srh4']  

        if (srch or srch2 or srch3 or srch4):
            actividades = Actividad.objects.all()

            
        
            if srch:
                dep = Dependencia.objects.get(pk=srch)  
                proper = ProgramaOperativo.objects.filter(dependencia=dep) 
                for i in proper: 
                    actividades = Actividad.objects.filter(programaoperativo=i)      

            # if srch3:
            #     obje = Objetivo.objects.get(pk=srch3)
            #     print("Objetivo", obje)
            #     depen = Dependencia.objects.filter(objetivo=obje) 
            #     print("Dependencias", depen)
            #     for j in depen:
            #         proper2 = ProgramaOperativo.objects.filter(dependencia=j)      
    
            #     print("Programas ", proper2)
            #     for x in proper2:
            #         actividades = actividades.filter(programaoperativo=x) 
            #         print("x", actividades)         
            
               
            actividades = actividades.filter(Q(estado__icontains=srch2))  

            for i in actividades:
                if (date_object.date() > i.fecha_in):
                    colores+= ['red'] 
                else:
                    colores+= ['green']
            
            contador = actividades.count() 
            evento =zip(actividades, colores)
            if actividades: 
                return render(request, 'users/calendario.html', {'actividad':evento, 'contador': contador,'fecha': formatedDay,'color':colores,'depende':depend,'total':actividades,'objetivo':objetivo})
            else:
                messages.error(request,'Resultados no encontrados')    
        else:
            return HttpResponseRedirect('usuarios/calendario/')     
    return render(request, 'users/calendario.html',{'actividad':evento,'fecha': formatedDay, 'contador': contador,'depende':depend, 'objetivo':objetivo})


class UsuarioView(LoginRequiredMixin,View):  
    login_url = 'login'
    def get(self, request):
        return render(request, 'index.html')



class LoginView(View):
    def post(self,request):
        username = str(request.POST['usuario'])
        password = str(request.POST['pass'])
        if username:
            user = authenticate(username=username,password=password)
            if user != None:
                login(request,user)
                return redirect(request.path) 
            else:
                messages.error(request,'Usuario o contraseña inválidos')
                return redirect('login')
                
            
        return render(request,"users/login.html")
        pass
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request,"users/login.html")
        pass


@login_required(login_url='login')
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

def vista_contrasena_olvidada(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'users/contrasenaolvidada.html')

class GraficaView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request, *args, **kwargs):
        return render(request, 'users/graficas.html', { })


class CharData(LoginRequiredMixin,APIView):
    login_url = 'login'
    authentication_classes = []
    permission_classes =[]

    def get(self, request, format=None):
        nom = 10
        apepat = 18
        apemat = 7
        ed = 2
        #Var
        nomb = 'Danza del Venado'
        desc = 'Evento artistico'
        programa= 'Eventos Culturales'
        preje='$12000'
        fechaini='2019-05-30'
        labels = ['IMDA', 'IMAC', 'SEDECO', 'IMJU']
        default_items = [nom,apepat,apemat,ed]
        title= 'Prueba'
        data ={
        "nombre": nomb,
        "descri": desc,
        "programa": programa,
        "pres": preje,
        "fecha":fechaini
        
        }
        return Response(data)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
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

@login_required(login_url='login')
def perfil_view(request):
    return render(request,'users/perfil.html')

class CambiarPassview(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        return render(request,'users/cambiarPass.html')
    def post(self,request):
        user = User.objects.get(pk=request.user.id)
        autenticar = authenticate(username=user.username,password=request.POST.get("passActual"))
        if autenticar:
            user.set_password(request.POST.get("nuevaPass"))
            user.save()
            messages.success(request,"Contraseña actualizada con éxito")
            return redirect('index')
        else:
            messages.error(request,"Contraseña incorrecta")
        return render(request,'users/cambiarPass.html')
