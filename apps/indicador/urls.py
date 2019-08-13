from django.conf.urls import url
from django.urls import path
from apps.indicador.views import *
# from .views import Actividad
urlpatterns = [
    path('indicador/capturar/metas', AccionesMetasView.as_view(),name='capturarMetasList'),
    path('indicador/capturar/metas/<str:idAccion>', AccionesMetasForm.as_view(),name='capturarMetasForm')
]
