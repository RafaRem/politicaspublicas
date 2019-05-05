from django.db import models
# Create your models here.
class Dependencia(models.Model):
    nombre = models.CharField(max_length=30, blank=True)
    director = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=30, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    tipo = models.CharField(max_length=30, blank=True)

class Departamento(models.Model):

    dependencia = models.ForeignKey(Dependencia,on_delete=models.CASCADE)

