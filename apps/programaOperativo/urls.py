from django.conf.urls import url
from apps.programaOperativo.views import ProgramasOperativosView
# from .views import Actividad
urlpatterns = [
    url(r'^programasOperativos/list', ProgramasOperativosView.as_view(), name="listaProgramasOperativos" )
    # path('/programasOperativos/<int:id>',IndexView.as_view(), name="editarProgramaOperativo" )    
]