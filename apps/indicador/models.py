from django.db import models

# Create your models here.


class ClasificacionGasto(models.Model):
    nombre = models.CharField(max_length=300)
    class Meta:
        verbose_name = 'Clasificadores de gastos'
    def __str__(self):
        return self.nombre
    def natural_key(self):
        return (self.nombre)

class ConceptoGasto(models.Model):
    nombre = models.CharField(max_length=300,verbose_name="Nombre de gasto")
    clasificacion = models.ForeignKey(ClasificacionGasto, on_delete=models.PROTECT,
    verbose_name = 'Clasificación del gasto')
    class Meta:
        verbose_name = 'Conceptos por gasto'
    def __str__(self):
        return self.nombre
    

class Escolaridad(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    class Meta:
        verbose_name = "Escolaridad"
    def __str__(self):
        return self.nombre

class GruposVulnerables(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    class Meta:
        verbose_name = 'Grupos vulnerables'
    def __str__(self):
        return self.nombre

class SectorSocial(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    class Meta:
        verbose_name = 'Sectores sociales'
    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    class Meta:
        verbose_name = 'Ubicación'
    def __str__(self):
        return self.nombre

class SectorEconomico(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    class Meta:
        verbose_name = 'Sectores económicos'
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
    def __str__(self):
        return self.nombre
