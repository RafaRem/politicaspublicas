from django.contrib import admin
# Register your models here.
from apps.dependencia.models import Departamento,Dependencia,Raiz
admin.site.register(Dependencia)
admin.site.register(Departamento)
admin.site.register(Raiz)