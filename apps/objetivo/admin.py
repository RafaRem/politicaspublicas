from django.contrib import admin
# Register your models here.
from apps.objetivo.models import Objetivo, DetallesObjetivo

@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nombre', 'tipo']
    ordering = ['numero']
    filter_horizontal = ('dependencia',)
    search_fields = ('nombre', 'tipo', 'numero')
    # actions = [make_published]

@admin.register(DetallesObjetivo)
class DetallesObjetivoAdmin(admin.ModelAdmin):
    list_display = ['objetivo', 'dependencia']




# admin.site.register(DetallesObjetivo)