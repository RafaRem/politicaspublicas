from django.db import models
from apps.dependencia.models import Dependencia
# Create your models here.


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
    
class Escolaridad(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    class Meta:
        verbose_name = "Escolaridad"
        verbose_name_plural = "Escolaridades"

    def __str__(self):
        return self.nombre

class GruposVulnerables(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    class Meta:
        verbose_name = 'Grupo vulnerable'
        verbose_name_plural = 'Grupos vulnerables'

    def __str__(self):
        return self.nombre

class SectorSocial(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    class Meta:
        verbose_name = 'Sector social'
        verbose_name_plural = 'Sectores sociales'
    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

    def __str__(self):
        return self.nombre

class SectorEconomico(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    class Meta:
        verbose_name = 'Sector económico'
        verbose_name_plural = 'Sectores económicos'

    def __str__(self):
        return self.nombre

class CategoriaPoblacion(models.Model):
    opcionesSexo = (
        ('h','Hombre'),
        ('m','Mujer'),
        ('a','Ambos')
    )
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    sexo = models.CharField(choices=opcionesSexo,max_length=30)
    edadDesde = models.CharField(max_length=20,verbose_name='Edad desde')
    edadHasta = models.CharField(max_length=20,verbose_name='Edad hasta')
    class Meta:
        verbose_name = 'Categoría de población'
        verbose_name_plural = 'Categorías de población'
    def __str__(self):
        return self.nombre

class Periodo(models.Model):
    nombre = models.CharField(max_length=300,verbose_name="Nombre del periodo")
    fechaInicial = models.DateField(verbose_name="Fecha de inicio")
    fechaFinal = models.DateField(verbose_name="Fecha de final")
    capturaHabilitada = models.BooleanField(verbose_name="Captura habilitada",default=True)
    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
    def __str__(self):
        return self.nombre
