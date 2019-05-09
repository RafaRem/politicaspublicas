from django.db import models
# Create your models here.
class Dependencia(models.Model):
    opcionesTipo = (
        ('d','Dependencia'),
        ('p','Paramunicipal')
    )
    nombre = models.CharField(max_length=100, blank=True)
    director = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=100, blank=True)
    tipo = models.CharField(max_length=30, choices=opcionesTipo, blank=True)
    def __str__(self):
        return self.nombre
    

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    dependencia = models.ForeignKey(Dependencia,on_delete=models.CASCADE)
    encargado = models.CharField(max_length=100)
    def __str__(self):
        return self.dependencia.nombre + ', ' + self.nombre
    