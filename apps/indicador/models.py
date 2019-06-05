from django.db import models

# Create your models here.

class CategoriaPoblacionObjetivo(models.Model):
    nombre = models.CharField(max_length=300)
    class Meta:
        verbose_name = 'Categoría de población objetivo'
    def __str__(self):
        return self.nombre

class PoblacionObjetivo(models.Model):
    opcionesSexo =(
        ('h','Hombre'),
        ('m', 'Mujer'),
        ('a', 'Ambos'),
        ('l', 'LGBT')
    )
    categoria = models.ForeignKey(CategoriaPoblacionObjetivo, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=300, verbose_name="Nombre")
    sexo = models.CharField(max_length=30,choices=opcionesSexo, verbose_name="Sexo")
    edadDesde = models.CharField(max_length=30, verbose_name="Edad desde")
    edadHasta = models.CharField(max_length=30, verbose_name="Edad hasta")
    class Meta:
        verbose_name = 'Población objetivo'
    def __str__(self):
        return self.nombre

class ClasificacionGasto(models.Model):
    nombre = models.CharField(max_length=300)
    class Meta:
        verbose_name = 'Clasificadores de gastos'
    def __str__(self):
        return self.nombre

class ConceptoGasto(models.Model):
    nombre = models.CharField(max_length=300,verbose_name="Nombre de gasto")
    clasificacion = models.ForeignKey(ClasificacionGasto, on_delete=models.PROTECT,
    verbose_name = 'Clasificación del gasto')
    class Meta:
        verbose_name = 'Conceptos por gasto'

