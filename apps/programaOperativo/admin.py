from django.contrib import admin
from apps.programaOperativo.models import *



@admin.register(ProgramaOperativo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'dependencia', 'objetivo']
    ordering = ['nombre']
    search_fields = ('nombre','dependencia__nombre',)


# admin.site.register(ProgramaOperativo)
admin.site.register(Actividad)


