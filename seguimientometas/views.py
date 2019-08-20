from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
"""MOdelos"""
from apps.indicador.models import PeriodoGobierno, Meta
from apps.programaOperativo.models import Acciones

class RenderView(TemplateView):
    template_name = ".html"
    