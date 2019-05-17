from django.contrib import admin
# Register your models here.
from apps.dependencia.models import Departamento,Dependencia,Raiz
admin.site.register(Departamento)
admin.site.register(Raiz)

@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    search_fields = ('nombre', 'tipo')