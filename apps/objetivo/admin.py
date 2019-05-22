from django.contrib import admin
# Register your models here.
from apps.objetivo.models import Objetivo

@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nombre', 'tipo']
    ordering = ['numero']
    filter_horizontal = ('dependencia',)
    search_fields = ['nombre']
    # actions = [make_published]





# admin.site.register(DetallesObjetivo)