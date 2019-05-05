from django.db import models
from apps.dependencia.models import *

# Create your models here.
class ObjetivoTransversal(models.Model):
    ejesTransversales = (
        ('1','Desarrollo Integral'),
        ('2','Desarrollo Social y Humano'),
        ('3','Promoción Económica y Medio Ambiente'),
        ('4','Seguridad Ciudadana y Protección Civil'),
        ('5','Combate a la Corrupción y Participación Ciudadana')
    )
    descripcion = models.CharField(max_length=300)
    meta = models.CharField(max_length=200,blank=True)
    estrategia = models.CharField(max_length=200, blank=True)
    ejeTransversal = models.CharField(max_length=30,choices=ejesTransversales)

#Esta clase es utilizada para incluir a varias dependencias en los objetivos transversales
class DetallesObjetivoTransversal(models.Model):
    objetivoTransversal = models.ForeignKey(ObjetivoTransversal,on_delete=models.CASCADE)
    dependencia = models.ForeignKey(Dependencia,on_delete=models.CASCADE)
    class Meta:
        unique_together=('objetivoTransversal','dependencia')
