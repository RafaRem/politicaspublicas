from django.conf.urls import url
from django.urls import path
from apps.dependencia.views import *
# from .views import Actividad
urlpatterns = [
    path('dependencia/programasoperativos', ProgramasOperativosList.as_view(), 
    name="dependencia_pos" ),
]
