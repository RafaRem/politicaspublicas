from django.contrib import admin
from apps.programaOperativo.models import *



@admin.register(ProgramaOperativo)
class ProgramaOperativoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'dependencia']
    list_display_links = ['id','nombre']
    ordering = ['nombre']
    search_fields = ('id', 'nombre','dependencia__nombre',)
    filter_horizontal = ('acciones',)

@admin.register(Acciones)
class AccionesAdmin(admin.ModelAdmin):
    list_display = ['id','nombre', 'objetivo']
    ordering = ['nombre',]
    filter_horizontal = ['escolaridad','gruposVulnerables', 'sectorSocial','sectorEconomico','ubicacion','categoriaPoblacion']
    search_fields = ['id', 'nombre']
# admin.site.register(ProgramaOperativo)
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'get_dependencia', 'estado', 'fechaRegistrada', 'fechaActualizada']
    ordering = ['nombre']
    search_fields = ['nombre']
    list_filter = ['programaoperativo__dependencia__nombre']
    def get_dependencia(self,obj):
        return obj.programaoperativo.dependencia.nombre
    get_dependencia.short_description = 'Dependencia'
    get_dependencia.admin_order_field = 'programaoperativo__dependencia__nombre'

    def get_accion(self,obj):
        return obj.accion.nombre
    get_accion.short_description = 'Acción'
    get_accion.admin_order_field = 'accion__nombre'

@admin.register(DetallesGasto)
class DetallesGastoAdmin(admin.ModelAdmin):
    list_display = ['id','gasto','accion','cantidad']
    ordering = ['accion']
    search_fields = ['id','accion__nombre', 'gasto__nombre']

