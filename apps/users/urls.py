from django.conf.urls import url
from apps.users.views import *
urlpatterns = [
    url(r'^usuario/zZx324DfgZc3223d/',LoginView.as_view(), name="login" ),
    url(r'^$', IndexView.as_view(), name="index" ),
    url(r'^usuario/registrar/',vista_registrar, name="registrar" ),
    url(r'^usuario/graficas/', GraficaView.as_view() , name="grafica" ),
    url(r'^usuario/data/', CharData.as_view(), name='data'),
    url(r'^usuario/reporte/', report, name='report'),
    url(r'^usuario/calendario/', CalendarView , name="calendar" ),
    url(r'^usuario/logout/',logout_view, name="logout" ),
    url(r'^usuario/forgottenpass/', vista_contrasena_olvidada, name="contraOlvidada" ),
    url(r'^usuario/perfil/', perfil_view, name="perfil" ),
    url(r'^usuario/cambiar-password/', CambiarPassview.as_view(), name="cambiarPass" ),
]