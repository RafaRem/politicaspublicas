from django.contrib import admin
# Register your models here.
from apps.dependencia.models import Departamento,Dependencia,Raiz
admin.site.register(Departamento)
admin.site.register(Raiz)

@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo')
    list_display_links = ['id','nombre']
    search_fields = ('nombre', 'tipo')
    # filter_horizontal = ('adscrita',)
    # fieldsets = (
    #     ('Dependencia', {
    #         "fields": (
    #             'nombre',
    #             'tipo'
    #         ),
    #     }),
    # )
    