from django.db import models
from apps.dependencia.models import *

# Create your models here.
class Objetivo(models.Model):
    opcionesEstado = (
        ('a','Activo'),
        ('a','Inactivo')
    )
    opcionesEjesTransversales = (
        ('1','Desarrollo Integral'),
        ('2','Desarrollo Social y Humano'),
        ('3','Promoción Económica y Medio Ambiente'),
        ('4','Seguridad Ciudadana y Protección Civil'),
        ('5','Combate a la Corrupción y Participación Ciudadana')
    )
    opcionesTipoObjetivo = (
        ('t', 'Transversal'),
        ('e', 'Estratégico')
    )
    numero = models.CharField(max_length=300,blank=True, null=True)
    nombre = models.CharField(max_length=300,blank=True)
    tipo = models.CharField(max_length=300,choices=opcionesTipoObjetivo)
    descripcion = models.CharField(max_length=1000, blank=True)
    meta = models.CharField(max_length=200,blank=True)
    estrategia = models.CharField(max_length=1000, blank=True)
    ejeTransversal = models.CharField(max_length=300,choices=opcionesEjesTransversales)
    dependencia = models.ManyToManyField(Dependencia,blank=True)
    estado = models.CharField(max_length=3,default='a',choices=opcionesEstado)
    class Meta:
        verbose_name = 'Objetivos transversales/estratégicos'
    def __str__(self):
        return self.numero + ',' + self.nombre
