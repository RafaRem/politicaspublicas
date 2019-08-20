from django.conf.urls import url
from django.urls import path
from apps.indicador.views import *
# from .views import Actividad
urlpatterns = [
    path('indicador/capturar/metas', AccionesMetasView.as_view(),name='capturarMetasList'),
    path('indicador/capturar/metas/<str:idAccion>', AccionesMetasForm.as_view(),name='capturarMetasForm'),
    path('indicador/fichas/accion/<str:idAccion>', FichaAccion.as_view(),name='fichaAccion'),
    path('indicador/configuraciones', Configuraciones.as_view(),name='configuraciones'),
]
