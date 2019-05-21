from django.urls import path
from apps.programaOperativo.views import ProgramasOperativos
# from .views import Actividad
urlpatterns = [
    path('/programasOperativos/list', ProgramasOperativos.as_view(), name="listaProgramasOperativos" )
    # path('/programasOperativos/<int:id>',IndexView.as_view(), name="editarProgramaOperativo" )    
]