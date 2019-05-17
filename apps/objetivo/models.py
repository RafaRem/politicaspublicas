from django.db import models
from apps.dependencia.models import *

# Create your models here.
class Objetivo(models.Model):
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
    numero = models.CharField(max_length=30,blank=True)
    nombre = models.CharField(max_length=100,blank=True)
    tipo = models.CharField(max_length=30,choices=opcionesTipoObjetivo)
    descripcion = models.CharField(max_length=300, blank=True)
    meta = models.CharField(max_length=200,blank=True)
    estrategia = models.CharField(max_length=200, blank=True)
    ejeTransversal = models.CharField(max_length=30,choices=opcionesEjesTransversales)
    def __str__(self):
        return self.numero + ',' + self.nombre
    

#Esta clase es utilizada para incluir a varias dependencias en los objetivos transversales
class DetallesObjetivo(models.Model):
    objetivo = models.ForeignKey(Objetivo,on_delete=models.CASCADE)
    dependencia = models.ForeignKey(Dependencia,on_delete=models.CASCADE)
    class Meta:
        unique_together=('objetivo','dependencia')
    def __str__(self):
        return self.objetivo.nombre + ', ' + self.dependencia.nombre
