from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
"""Models"""
from apps.programaOperativo.models import ProgramaOperativo


# Create your views here.
class ProgramasOperativosList(LoginRequiredMixin,View):
    """Will show all the department's operative programs"""
    login_url = 'login'
    def get(self,request):
        programasOperativos = ProgramaOperativo.objects.filter(estado='a',dependencia=request.user.profile.dependencia)
        return render(request,'dependencias/programasoperativos.html')

