from django.db import models
from apps.objetivo.models import *
"""Modelos"""
from apps.objetivo.models import Objetivo
from apps.dependencia.models import *
from django.contrib.auth.models import User
from apps.indicador.models import PoblacionObjetivo

# Create your models here.
class Acciones(models.Model):
    nombre = models.CharField(max_length=700)
    objetivo = models.ForeignKey(Objetivo,on_delete=models.PROTECT)
    poblacionObjetivo = models.ForeignKey(PoblacionObjetivo,on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'Acciones de programas operativos'
    def __str__(self):
        return self.nombre
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
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Descripción')
    tipoPrograma = models.CharField(max_length=30,choices=opcionesTipoPrograma, blank=True, null=True, 
    verbose_name='Tipo de programa')
    objetivos = models.CharField(max_length=1000,blank=True, null=True, verbose_name='Objetivos')
    estrategias = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Estrategias')
    beneficiarios = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Beneficiarios')
    justificacion = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Justificación')
    problematicaSocial = models.CharField(max_length=1000, blank=True, null=True, verbose_name = 'Problemática social')
    #BORRAR OBJETIVO AL MANDAR A PRODUCCION
    objetivo = models.ForeignKey(Objetivo, on_delete=models.PROTECT)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.PROTECT)
    acciones = models.ManyToManyField(Acciones, blank=True)
    estado = models.CharField(choices=opcionesEstado,max_length=30,default='a')
    class Meta:
        verbose_name = 'Programas operativos'
    def __str__(self):
        return self.nombre



class Actividad(models.Model):
    opcionesEstado = (
        ('p','Programada'),
        ('t','Terminada'),
        ('i','Inactiva'),
        ('r','Revisada'),
        ('n', 'No válida')
    )
    user = models.ForeignKey(User, on_delete= models.PROTECT)
    programaoperativo = models.ForeignKey(ProgramaOperativo, on_delete = models.PROTECT)
    nombre = models.CharField(max_length=100, 
    verbose_name="¿Qué actividad se realiza?")
    descripcion = models.TextField(max_length=300, 
    verbose_name="Descripción breve")
    presupuestoProgramado = models.CharField(max_length=300, 
    verbose_name="Presupuesto asignado a esta actividad")
    presupuestoEjercido = models.CharField(max_length=300,blank=True, null=True,
    verbose_name="Presupuesto ejercido")
    personasInvolucradas = models.CharField(max_length=10,blank=True, null=True,
    verbose_name="Personas involucradas")
    evidencia = models.FileField(blank=True, null=True)
    fecha_in = models.DateField(verbose_name="Día en el que se realiza")
    fecha_fi = models.DateField(verbose_name="Día en el que se finaliza")
    latitud = models.CharField(max_length=300, blank=True, null=True)
    longitud = models.CharField(max_length=300, blank=True, null=True)
    accion = models.ForeignKey(Acciones, on_delete=models.PROTECT, 
    verbose_name="Acción a la que corresponde")
    created = models.DateTimeField(auto_now_add=True)    
    estado = models.CharField(choices=opcionesEstado,max_length=30,default='p')
    class Meta:
        verbose_name = 'Actividades'
    def __str__(self):
        return self.nombre


    


    


