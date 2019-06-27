from django.conf.urls import url
from django.urls import path
from apps.programaOperativo.views import *
# from .views import Actividad
urlpatterns = [
    path('programasOperativos/post/<int:idPo>', ProgramasOperativosView.as_view(), name="postPo" ),
    path('programasOperativos/list/<int:idObjetivo>', ProgramasOperativosListView.as_view(), name="listPoObjetivo" ),
    #"""Esta url es solo para obtener acciones por programa operativo, no es api"""
    path('programasOperativos/get/aciones/<int:idPo>', get_acciones_po_view, name="getAccioesPo"),
    #De aquí en adelante on las actividades
    path('programasOperativos/accion/ver/<str:idAccion>', ver_accion, name='verAccion'),
    path('programasOperativos/accion/capturar-gastos/<str:idAccion>/<str:idPeriodo>', CapturarGastoView.as_view(), name='capturarGastos'),
    path('programasOperativos/accion/ver/gastos/<str:idAccion>/<str:idPeriodo>', ver_gastos, name='verGastos'),
    path('programasOperativos/accion/editar/gastos/<str:idAccion>/<str:idPeriodo>', EditarGastosView.as_view(), name='editarGastos'),
    #Actividades
    path('programasOperativos/actividad/nueva', ActividadFormView.as_view() , name="nuevaActividad" ),
    path('programasOperativos/actividad/lista', ActividadesListView.as_view(), name='listActividades'),
    path('programasOperativos/actividad/terminar/<str:idActividad>', 
    TerminarActividadFormView.as_view(), name='terminarActividad'),
    path('programasOperativos/actividad/ver/<str:idActividad>', ver_actividad, name='verActividad'),
    path('programasOperativos/actividad/reporte/enlace', ReporteActividadesEnlaceView.as_view(),
     name='reporteActividadEnlace'),
    
]
