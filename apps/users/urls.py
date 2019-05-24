from django.conf.urls import url
from apps.users.views import *
urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index" ),
    url(r'^usuario/login/',LoginView.as_view(), name="login" ),
    url(r'^usuario/registrar/',vista_registrar, name="registrar" ),
    url(r'^usuario/graficas/', GraficaView.as_view() , name="grafica" ),
    url(r'^usuario/data/', CharData.as_view(), name='data'),
    url(r'^usuario/reporte/', report, name='report'),
    url(r'^usuario/calendario/', CalendarView , name="calendar" ),
    url(r'^usuario/logout/',logout_view, name="logout" ),
    # url(r'^login/', vista_login, name="login" ),
    # url(r'^usuarios/registrar',vista_registrar , name="registrar" ),
    # url(r'^logout/',vista_logout,name='logout'),
    # url(r'^regEx/',vista_regex,name='regEx'),
    # url(r'^json/correoDisponible',vista_json_correoDisponible,name='correoDisponible'),
    # url(r'^ajax/autenticar',vista_ajax_autenticar,name='autenticar'),
    # url(r'^inmueble/tus-inmuebles',vista_tus_inmuebles,name="tusInmuebles"),
    # url(r'^usuarios/perfil',vista_updateProfile , name="actualizarPerfil" ),
]