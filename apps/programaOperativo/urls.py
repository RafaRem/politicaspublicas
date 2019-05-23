from django.conf.urls import url
from django.urls import path
from apps.programaOperativo.views import ProgramasOperativosView,ProgramasOperativosListView
# from .views import Actividad
urlpatterns = [
    path('programasOperativos/post/<int:idPo>', ProgramasOperativosView.as_view(), name="postPo" ),
    path('programasOperativos/list/<int:idObjetivo>', ProgramasOperativosListView.as_view(), name="listPoObjetivo" ),

]
