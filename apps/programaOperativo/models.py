from django.db import models
from apps.objetivo.models import *
"""Modelos"""
from apps.objetivo.models import Objetivo
from apps.dependencia.models import *
from apps.indicador.models import *
from django.contrib.auth.models import User 
from apps.indicador.models import ConceptoGasto,Periodo,Meta,PeriodoGobierno
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
    indicador = models.ManyToManyField(Indicador, blank=True)
    meta = models.ManyToManyField(Meta,blank=True)
    publica = models.BooleanField(default=True, verbose_name='¿Es una acción pública?')
    cualitativa = models.BooleanField(default=False,verbose_name='¿Es una acción cualitativa?')
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
    departamento = models.ForeignKey(Departamento,blank=True, null=True, 
    on_delete=models.PROTECT, verbose_name="Departamento")
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
        ('r','Principal'),
        ('s','Secundaria'),
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
    multiplicador = models.IntegerField(default=1)
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
    def __str__(self):
        return self.nombre
    def save(self, usuario=None, estado="", *args, **kwargs):
        if usuario:
            usuario = User.objects.get(pk=usuario)
            log = LogActividad.objects.create(usuario=usuario,actividad=self, estado=estado)
            log.save()
            pass
 
        super().save(*args, **kwargs)  
        # Call the "real" save() method.

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
        unique_together = ['accion','gasto','periodo']
    def __str__(self):
        return (self.accion.nombre + ', ' + self.gasto.nombre)

class LogActividad(models.Model):
    opcionesEstado = (
        ('p','Programada'),
        ('t','Por revisar'),
        ('i','Inactiva'),
        ('r','Válida'),
        ('n', 'No válida')
    )
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    actividad = models.ForeignKey(Actividad, on_delete=models.PROTECT)
    estado = models.CharField(choices=opcionesEstado,max_length=30,default='p')
    created = models.DateTimeField(auto_now_add=True)    

class GastoAnualAsignado(models.Model):
    programaOperativo = models.ForeignKey(ProgramaOperativo,on_delete=models.PROTECT,
    verbose_name="Programa operativo")
    cantidad = models.FloatField(verbose_name="Cantidad asignada")
    periodoGobierno = models.ForeignKey(PeriodoGobierno,on_delete=models.PROTECT,
    verbose_name="Gasto asignado al periodo")
    permitirModificar = models.BooleanField(verbose_name="¿Permitir modificar?",default=True)
    class Meta:
        verbose_name = "Gasto anual asignado"
        verbose_name_plural = "Gastos anuales asignados"
        unique_together = ['programaOperativo', 'periodoGobierno']
    def __str__(self):
        return self.programaOperativo.nombre
    

