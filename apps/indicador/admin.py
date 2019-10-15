from django.contrib import admin
from apps.indicador.models import *
# Register your models here.

@admin.register(ClasificacionGasto)
class ClasificacionGastoAdmin(admin.ModelAdmin):
    list_display = ['id','nombre']
    ordering = ['nombre']
    search_fields = ['nombre']

@admin.register(ConceptoGasto)
class ConceptoGastoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'clasificacion']
    ordering = ['nombre']
    search_fields = ['nombre']

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ['id','nombre','fechaInicial', 'fechaFinal']

@admin.register(PeriodoGobierno)
class PeriodoGobiernoAdmin(admin.ModelAdmin):
    list_display = ['descripcion','fechaInicial','fechaFinal']

@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']
    search_fields = ['nombre']

