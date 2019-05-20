from django.conf.urls import url
from apps.users.views import *
from apps.programaOperativo.views import Actividad
urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index" ),
    url(r'^login/',LoginView.as_view(), name="login" ),
    url(r'^registrar/',vista_registrar, name="registrar" ),
    url(r'^graficas/', GraficaView.as_view() , name="grafica" ),
    url(r'^data/', CharData.as_view(), name='data'),
    url(r'^reporte/', report, name='report'),
    url(r'^calendario/', CalendarView.as_view() , name="calendar" ),
    url(r'^RegistroActividad/', Actividad, name="Regactividad" ),
    url(r'^logout/',logout_view, name="logout" ),
    url(r'^middleware/',vista_middleware_ejemplo, name="middleware" ),

    # url(r'^login/', vista_login, name="login" ),
    # url(r'^usuarios/registrar',vista_registrar , name="registrar" ),
    # url(r'^logout/',vista_logout,name='logout'),
    # url(r'^regEx/',vista_regex,name='regEx'),
    # url(r'^json/correoDisponible',vista_json_correoDisponible,name='correoDisponible'),
    # url(r'^ajax/autenticar',vista_ajax_autenticar,name='autenticar'),
    # url(r'^inmueble/tus-inmuebles',vista_tus_inmuebles,name="tusInmuebles"),
    # url(r'^usuarios/perfil',vista_updateProfile , name="actualizarPerfil" ),
]