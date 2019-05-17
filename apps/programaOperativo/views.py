from django.shortcuts import render, redirect
from django.contrib import messages
#Views
from django.views.generic import View
from apps.users.forms import RegistrarActividad
# Create your views here.
def Actividad(request):
    if request.method=='POST':
        form = RegistrarActividad(request.POST)
        if form.is_valid():
                messages.success(request,"Registro con exito")
                form.save()
        return redirect("Regactividad")
    else:
        form = RegistrarActividad()
    return render(request,'users/RegistroActividad.html',{})