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
    filter_horizontal = ['meta']
    search_fields = ['id', 'nombre']
# admin.site.register(ProgramaOperativo)
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'get_dependencia', 'estado', 'fechaRegistrada', 'fechaActualizada']
    ordering = ['nombre']
    search_fields = ['nombre']
    list_filter = ['programaoperativo__dependencia__nombre', 'estado']
    def get_dependencia(self,obj):
        return obj.programaoperativo.dependencia.nombre
    get_dependencia.short_description = 'Dependencia'
    get_dependencia.admin_order_field = 'programaoperativo__dependencia__nombre'

    def get_accion(self,obj):
        return obj.accion.nombre
    get_accion.short_description = 'Acción'
    get_accion.admin_order_field = 'accion__nombre'
    def save_model(self, request, obj, form, change):
        # print(form.get('estado'))
        log = LogActividad.objects.create(
        usuario=request.user,
        actividad=obj, 
        estado=request.POST.get('estado'))
        log.save()
        obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(DetallesGasto)
class DetallesGastoAdmin(admin.ModelAdmin):
    list_display = ['id','gasto','accion','cantidad']
    ordering = ['accion']
    search_fields = ['id','accion__nombre', 'gasto__nombre']

@admin.register(LogActividad)
class LogActividadAdmin(admin.ModelAdmin):
    list_display = ['getActividadId' ,'usuario', 'actividad', 'estado', 'created']
    search_fields = ['actividad__id','usuario__username']
    def getActividadId(self,obj):
        return obj.actividad.id
    getActividadId.short_description = 'ID'
    getActividadId.admin_order_field = 'actividad__id'

@admin.register(GastoAnualAsignado)
class GastoAnualAsignadoAdmin(admin.ModelAdmin):
    list_display = ['programaOperativo','get_dependencia', 'periodoGobierno']
    def get_dependencia(self,obj):
        return obj.programaOperativo.dependencia.nombre
    get_dependencia.short_description = 'Dependencia'
    get_dependencia.admin_order_field = 'programaoperativo__dependencia__nombre'
