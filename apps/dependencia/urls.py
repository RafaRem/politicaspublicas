from django.conf.urls import url
from django.urls import path
from apps.dependencia.views import *
# from .views import Actividad
urlpatterns = [
    path('dependencia/programasoperativos', ProgramasOperativosList.as_view(), 
    name="dependencia_pos" ),
    path('dependencia/presupuesto-anual/<str:idProgramaOperativo>', PresupuestoAnualList.as_view(), 
    name="presupuestoAnual" ),
    path('dependencia/acciones/<str:idDependencia>', AccionesDependencia.as_view(), 
    name="accionesDependencia" ),
    path('dependencia/admin/list', DependenciasAdmin.as_view(), 
    name="dependenciasAdmin" ),
    path('depedencia/acciones-metas',accionesMetas,name='accionesMetas')
    
]
