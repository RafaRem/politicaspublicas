from django.db import models
from apps.objetivo.models import *
from django.contrib.auth.models import User

# Create your models here.
class ProgramaOperativo(models.Model):
    opcionesTipoPrograma=(
        ('i', 'Institucional'),
        ('e', 'Enfocado'),
        ('d', 'Distintivo'),
        ('p', 'Piloto'),
        ('f', 'Foro'),
        ('c', 'Campaña')
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=600)
    tipoPrograma = models.CharField(max_length=30,choices=opcionesTipoPrograma)
    objetivos = models.CharField(max_length=600)
    estrategias = models.CharField(max_length=600)
    beneficiarios = models.CharField(max_length=600)
    justificacion = models.CharField(max_length=600)
    problematicaSocial = models.CharField(max_length=600)
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    

class Actividad(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    programaoperativo = models.ForeignKey(ProgramaOperativo, on_delete = models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=300)
    fecha_in = models.DateField()
    fecha_fi = models.DateField()
    def __str__(self):
        return self.nombre