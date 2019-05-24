from django.conf.urls import url
from django.urls import path
from apps.programaOperativo.views import *
# from .views import Actividad
urlpatterns = [
    path('programasOperativos/post/<int:idPo>', ProgramasOperativosView.as_view(), name="postPo" ),
    path('programasOperativos/list/<int:idObjetivo>', ProgramasOperativosListView.as_view(), name="listPoObjetivo" ),
    path('programasOperativos/actividad/nueva', ActividadFormView.as_view() , name="nuevaActividad" ),
    #"""Esta url es solo para obtener acciones por programa operativo, no es api"""
    path('programasOperativos/get/aciones/<int:idPo>', get_acciones_po_view, name="getAccioesPo"),
]
