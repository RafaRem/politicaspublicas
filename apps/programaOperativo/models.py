from django.db import models
from apps.objetivoTransversal.models import *

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
    tipoPrograma = models.CharField(max_lenght=30,choices=opcionesTipoPrograma)
    objetivos = models.CharField(max_length=600)
    estrategias = models.CharField(max_length=600)
    beneficiarios = models.CharField(max_length=600)
    justificacion = models.CharField(max_length=600)
    problematicaSocial = models.CharField(max_lenth=600)
    objetivoTransversal = models.ForeignKey(ObjetivoTransversal, on_delete=models.CASCADE)
    
