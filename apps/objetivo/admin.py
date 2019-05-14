from django.contrib import admin
# Register your models here.
from apps.objetivo.models import Objetivo, DetallesObjetivo

admin.site.register(Objetivo)
admin.site.register(DetallesObjetivo)