from django.conf.urls import url
from django.urls import path
from apps.indicador.views import *
# from .views import Actividad
urlpatterns = [
    path('indicador/capturar/metas', AccionesMetasView.as_view(),name='capturarMetasList'),
    path('indicador/capturar/metas/<str:idAccion>', AccionesMetasForm.as_view(),name='capturarMetasForm'),
    path('indicador/fichas/accion/<str:idAccion>', FichaAccion.as_view(),name='fichaAccion'),
    path('indicador/fichas/programa/<str:idPrograma>', FichaProgramaOperativo.as_view(),name='fichaPrograma'),
    path('indicador/fichas/dependencia/<str:idDependencia>', FichaDependencia.as_view(),name='fichaDependencia'),
    path('indicador/fichas/objetivo/<str:idObjetivo>', FichaObjetivo.as_view(),name='fichaObjetivo'),
    path('indicador/fichas/eje/<str:idEje>', FichaEje.as_view(),name='fichaEje'),
    path('indicador/configuraciones', Configuraciones.as_view(),name='configuraciones'),
    path('indicador/admin/fichas', FichasAdmin.as_view(),name='fichasAdmin'),
    path('generarVariables',generar_variables, name='generarVariables')

]
