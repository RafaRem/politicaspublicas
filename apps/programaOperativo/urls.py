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
    path('programasOperativos/accion/editar/metas/<str:idAccion>', EditarMetasView.as_view(), name='capturarMetas'),
    #Actividades
    path('programasOperativos/actividad/nueva/<idProgramaOperativo>', ActividadFormView.as_view() , name="nuevaActividad" ),
    path('programasOperativos/actividad/lista', ActividadesListView.as_view(), name='listActividades'),
    path('programasOperativos/actividad/terminar/<str:idActividad>', 
    TerminarActividadFormView.as_view(), name='terminarActividad'),
    path('programasOperativos/actividad/revalidar/<str:idActividad>', 
    RevalidarActividadFormView.as_view(), name='revalidarActividad'),
    path('programasOperativos/actividad/ver/<str:idActividad>', ver_actividad, name='verActividad'),
    path('programasOperativos/actividad/enlace/reporte', ReporteActividadesEnlaceView.as_view(),
     name='reporteActividadEnlace'),
    path('programasOperativos/actividad/admin/list/actividades', ListActividadesAdmin.as_view(),
     name='listActividadesAdmin'),
    path('programasOperativos/actividad/admin/ver/actividad/<str:idActividad>', VerActividadAdmin.as_view(),
     name='verActividadAdmin'),
    path('programasOperativos/actividad/admin/reporte', ReporteActividadesAdmin.as_view(),
     name='reporteActividadesAdmin'),
    path('programasOperativos/actividad/admin/productividad', ProductividadAdmin.as_view(),
     name='productividadAdmin'),
    path('programasOperativos/actividad/admin/metas', MetasAdmin.as_view(),
     name='metasAdmin'),
    path('programasOperativos/actividad/escogerPo',escoger_po,name='escogerPo'),
]
