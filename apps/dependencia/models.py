from django.db import models
# Create your models here.
class Dependencia(models.Model):
    nombre = models.CharField(max_length=30, blank=True)
    director = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=30, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    tipo = models.CharField(max_length=30, blank=True)

class Departamento(models.Model):
<<<<<<< HEAD
    nombre = models.CharField(max_length=100)
    dependencia = models.ForeignKey(Dependencia,on_delete=models.CASCADE)
=======
    dependencia = models.ForeignKey(Dependencia,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
>>>>>>> c4e8c1a0a2f07117e9c8599d5aba807af7c58d5e
    encargado = models.CharField(max_length=100)

