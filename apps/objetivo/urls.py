from django.conf.urls import url
from apps.objetivo.views import ObjetivosView
# from .views import Actividad
urlpatterns = [
    url(r'^objetivos/list', ObjetivosView.as_view(), name="listaObjetivos" )
]