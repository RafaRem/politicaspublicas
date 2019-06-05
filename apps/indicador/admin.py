from django.contrib import admin
from apps.indicador.models import *
# Register your models here.

@admin.register(CategoriaPoblacionObjetivo)
class CategoriaPoblacionObjetivoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    ordering = ['nombre']
    search_fields = ['nombre']

@admin.register(PoblacionObjetivo)
class PoblacionObjetivoAdmin(admin.ModelAdmin):
    list_display = ['nombre','categoria','sexo']
    ordering = ['nombre']
    search_fields = ['nombre']

@admin.register(ClasificacionGasto)
class ClasificacionGastoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    ordering = ['nombre']
    search_fields = ['nombre']

@admin.register(ConceptoGasto)
class ConceptoGastoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'clasificacion']
    ordering = ['nombre']
    search_fields = ['nombre']

