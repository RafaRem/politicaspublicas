from django.contrib import admin
from apps.indicador.models import *
# Register your models here.

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

@admin.register(Escolaridad)
class EscolaridadAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(GruposVulnerables)
class GruposVulnerablesAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(SectorSocial)
class SectorSocialAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(CategoriaPoblacion)
class CategoriaPoblacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'edadDesde', 'edadHasta']

@admin.register(SectorEconomico)
class SectorEconomicoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
