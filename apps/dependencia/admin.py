from django.contrib import admin
# Register your models here.
from apps.dependencia.models import Departamento,Dependencia,Raiz,Alcance
admin.site.register(Raiz)


@admin.register(Alcance)
class AlcanceAdmin(admin.ModelAdmin):
    list_display=['id','nombre']
    list_display_links=['id','nombre']
    search_fields=['nombre']

@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo')
    list_display_links = ['id','nombre']
    search_fields = ('nombre', 'tipo')
    filter_horizontal=['alcance']
    # filter_horizontal = ('adscrita',)
    # fieldsets = (
    #     ('Dependencia', {
    #         "fields": (
    #             'nombre',
    #             'tipo'
    #         ),
    #     }),
    # )

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['id','nombre', 'dependencia']
    list_display_links = ['id','nombre']
    search_fields = ['id','nombre','dependencia__nombre']