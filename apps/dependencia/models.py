from django.db import models
from apps.indicador.models import Beneficiarios

# Este modelo es padre de una dependencia
class Raiz(models.Model):
    opcionesRaiz = (
        ('s','Secretaría'),
        ('g', 'Dirección general'),
        ('o','Otro')
    )
    nombre = models.CharField(max_length=100,blank=True, null=True)
    tipo = models.CharField(max_length=30,choices=opcionesRaiz)
    responsable = models.CharField(max_length=100,blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=5,default='A')
    class Meta:
        verbose_name = 'Secretaría/Dirección General'
        verbose_name_plural = 'Secretarías/Direcciones Generales'

    def __str__(self):
        return self.nombre
    
class Dependencia(models.Model):
    opcionesTipo = (
        ('d','Dependencia'),
        ('p','Paramunicipal')
    )
    opcionesEstado = (
        ('a', 'Activo'),
        ('i', 'Inactivo')
    )
    nombre = models.CharField(max_length=100, blank=True)
    director = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=100, blank=True)
    tipo = models.CharField(max_length=30, choices=opcionesTipo, blank=True)
    adscrita = models.ForeignKey(Raiz,blank=True, null=True, on_delete=models.PROTECT)
    estado = models.CharField(max_length=30,choices=opcionesEstado,default='a')
    tieneDepartamentos = models.BooleanField(verbose_name='¿Tiene departamentos?',default=True)
    beneficiarios = models.ManyToManyField(Beneficiarios ,blank=True, 
    verbose_name="Beneficiarios de la dependencia")
    class Meta:
        verbose_name = 'Dependencia'
        verbose_name_plural='Dependencias'
    def __str__(self):
        return self.nombre
    
class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    dependencia = models.ForeignKey(Dependencia,on_delete=models.PROTECT)
    encargado = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre



