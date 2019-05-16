from django.contrib import admin
# Register your models here.
from apps.objetivo.models import Objetivo, DetallesObjetivo


class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nombre', 'tipo']
    ordering = ['numero']
    # actions = [make_published]
admin.site.register(Objetivo, ObjetivoAdmin)
admin.site.register(DetallesObjetivo)