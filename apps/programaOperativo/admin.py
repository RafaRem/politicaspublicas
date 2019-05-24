from django.contrib import admin
from apps.programaOperativo.models import *



@admin.register(ProgramaOperativo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'dependencia', 'objetivo']
    ordering = ['nombre']
    search_fields = ('nombre','dependencia__nombre',)
    filter_horizontal = ('acciones',)

@admin.register(Acciones)
class AccionesAdmin(admin.ModelAdmin):
    list_display = ['nombre',]
    ordering = ['nombre',]
    search_fields = ['nombre']
# admin.site.register(ProgramaOperativo)
admin.site.register(Actividad)


