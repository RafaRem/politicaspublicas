from django.db import models
from apps.dependencia.models import Dependencia
# Create your models here.
class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Unidad de medida'
        verbose_name_plural = 'Unidades de medida'
    def __str__(self):
        return self.nombre

class Variable(models.Model):
    nombre = models.CharField(max_length=500)
    unidadMedida = models.ForeignKey(UnidadMedida, 
    on_delete=models.PROTECT ,blank=True, null=True)
    class Meta:
        verbose_name = 'Variable de medición'
        verbose_name_plural = 'Variables de medición'
    def __str__(self):
        return self.nombre
    
class ClasificacionGasto(models.Model):
    nombre = models.CharField(max_length=300)
    class Meta:
        verbose_name = 'Clasificadores de gastos'
        verbose_name_plural = 'Clasificadores de gastos'
    def __str__(self):
        return self.nombre
    def natural_key(self):
        return (self.nombre)

class ConceptoGasto(models.Model):
    opcionesTipo = (
        ('d','Dependencia'),
        ('p','Paramunicipal')
    )
    nombre = models.CharField(max_length=300,verbose_name="Nombre de gasto")
    clasificacion = models.ForeignKey(ClasificacionGasto, on_delete=models.PROTECT,
    verbose_name = 'Clasificación del gasto')
    #CUANDO EL TIPO ES DEPENDENCIA, SE USARÁN TODOS LOS CONCEPTOS CON TIPO DEPENDENCIA
    #CUANDO SEA PARAMUNICIPAL, SE CARGARÁN SOLO LOS DE ESA PARAMUNICIPAL
    tipoDependencia = models.CharField(max_length=30, choices=opcionesTipo, default='d')
    dependencia = models.ForeignKey(Dependencia,blank=True, null=True, on_delete=models.CASCADE,verbose_name='Dependencia a la que pertenece') 
    class Meta:
        verbose_name = 'Concepto por gasto'
        verbose_name_plural = 'Conceptos por gasto'
    def __str__(self):
        return self.nombre

class Periodo(models.Model):
    nombre = models.CharField(max_length=300,verbose_name="Nombre del periodo")
    fechaInicial = models.DateField(verbose_name="Fecha de inicio")
    fechaFinal = models.DateField(verbose_name="Fecha de final")
    capturaHabilitada = models.BooleanField(verbose_name="Captura habilitada",default=True)
    class Meta:
        verbose_name = 'Periodo de gastos'
        verbose_name_plural = 'Periodos de gastos'
    def __str__(self):
        return self.nombre

class PeriodoGobierno(models.Model):
    descripcion = models.CharField(max_length=300,verbose_name="Descripción del periodo")
    fechaInicial = models.DateField(verbose_name="Fecha de inicio del periodo")
    fechaFinal = models.DateField(verbose_name="Fecha fianl del periodo")
    permitirCambios = models.BooleanField(default=True,verbose_name="¿Permitir cambios?")
    class Meta:
        verbose_name= 'Periodo de gobierno'
        verbose_name_plural = 'Periodos de gobierno'
    def __str__(self):
        return self.descripcion

#TO:DO borrar
class Meta(models.Model):
    descripcion = models.CharField(max_length=300,verbose_name="Descripción de la meta")
    descendente = models.BooleanField(default=False,verbose_name="¿Es descendente?")
    noPublica = models.BooleanField(default=False, verbose_name="¿No es pública?")
    meta = models.IntegerField(verbose_name="Meta de número de actividades")
    periodo = models.ForeignKey(PeriodoGobierno,on_delete=models.PROTECT,verbose_name="Periodo de gobierno")
    class Meta:
        verbose_name= 'Meta de actividad'
        verbose_name_plural = 'Metas de actividades'
    def __str__(self):
        return str(self.id) + ',' + self.descripcion

class Configuracion(models.Model):
    periodoGobierno = models.ForeignKey(PeriodoGobierno, blank=True, null=True,
    on_delete=models.PROTECT, verbose_name="Periodo de gobierno a graficar")
