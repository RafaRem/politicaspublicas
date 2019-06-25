from django.db import models
from apps.objetivo.models import *
"""Modelos"""
from apps.objetivo.models import Objetivo
from apps.dependencia.models import *
from apps.indicador.models import *
from django.contrib.auth.models import User
from apps.indicador.models import ConceptoGasto,Periodo

# Create your models here.
class Acciones(models.Model):
    nombre = models.CharField(max_length=700)
    objetivo = models.ForeignKey(Objetivo,on_delete=models.PROTECT)
    escolaridad = models.ManyToManyField(Escolaridad, blank=True)
    gruposVulnerables = models.ManyToManyField(GruposVulnerables, blank=True)
    sectorSocial = models.ManyToManyField(SectorSocial, blank=True)
    sectorEconomico = models.ManyToManyField(SectorEconomico, blank=True)
    ubicacion = models.ManyToManyField(Ubicacion, blank=True)
    categoriaPoblacion = models.ManyToManyField(CategoriaPoblacion, blank=True)
    class Meta:
        verbose_name = 'Acción de programa operativo'
        verbose_name_plural = 'Acciones de programas operativos'
    def __str__(self):
        return str(self.id)+ ',' + self.nombre

class ProgramaOperativo(models.Model):
    opcionesTipoPrograma=(
        ('i', 'Institucional'),
        ('e', 'Enfocado'),
        ('d', 'Distintivo'),
        ('p', 'Piloto'),
        ('f', 'Foro'),
        ('c', 'Campaña')
    )
    opcionesEstado = (
        ('a','Activo'),
        ('i','Inactivo')
    )
    nombre = models.CharField(max_length=300)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.PROTECT)
    acciones = models.ManyToManyField(Acciones, blank=True)
    estado = models.CharField(choices=opcionesEstado,max_length=30,default='a')
    class Meta:
        verbose_name = 'Programa operativo'
        verbose_name_plural = 'Programas operativos'
    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    opcionesEstado = (
        ('p','Programada'),
        ('t','Por revisar'),
        ('i','Inactiva'),
        ('r','Válida'),
        ('n', 'No válida')
    )
    user = models.ForeignKey(User, on_delete= models.PROTECT)
    programaoperativo = models.ForeignKey(ProgramaOperativo, on_delete = models.PROTECT)
    nombre = models.CharField(max_length=500, 
    verbose_name="Actividad")
    descripcion = models.TextField(max_length=1000, 
    verbose_name="Descripción breve")
    personasInvolucradas = models.CharField(max_length=10,blank=True, null=True,
    verbose_name="Personal involucrado")
    beneficiarios = models.CharField(max_length=10,blank=True, null=True,
    verbose_name="Número de beneficiarios/Asistentes")
    evidencia = models.FileField(blank=True, null=True)
    fecha_in = models.DateField(verbose_name="Día en el que se realiza")
    fecha_fi = models.DateField(verbose_name="Día en el que se finaliza")
    latitud = models.CharField(max_length=300, blank=True, null=True)
    longitud = models.CharField(max_length=300, blank=True, null=True)
    accion = models.ForeignKey(Acciones, on_delete=models.PROTECT, 
    verbose_name="Acción a la que corresponde")
    created = models.DateTimeField(auto_now_add=True)    
    estado = models.CharField(choices=opcionesEstado,max_length=30,default='p')
    observaciones = models.CharField(max_length=800,blank=True, null=True)
    fechaRegistrada = models.DateTimeField(auto_now_add=True)
    fechaActualizada = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
    def __str__(self):
        return self.nombre

class DetallesGasto(models.Model):
    cantidad = models.CharField(max_length=100, 
    verbose_name="Cantidad")
    accion = models.ForeignKey(Acciones,on_delete=models.PROTECT,
    verbose_name="Acción")
    gasto = models.ForeignKey(ConceptoGasto,on_delete=models.PROTECT,
    verbose_name="Concepto de gasto")
    periodo = models.ForeignKey(Periodo,on_delete=models.PROTECT, 
    verbose_name="Periodo del gasto")
    class Meta:
        verbose_name = 'Detalle de gasto por acción'
        verbose_name_plural = 'Detalles de gasto por acción'
        unique_together = ['accion','gasto']
    def __str__(self):
        return (self.actividad.nombre + ', ' + self.gasto.nombre)
