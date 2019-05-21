"""seguimientometas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static  import static
from django.views.static import serve
from apps.users import urls as usersUrls
from apps.programaOperativo import urls as posUrls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^',include(usersUrls)),
    url(r'^',include(posUrls)),
    #url(r'^',include(ProgramUrls)),
    # url(r'^',include('apps.inmueble.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#este código es utilizado para subir archivos
# urlpatterns += [
#     url(r'^(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
# ]
