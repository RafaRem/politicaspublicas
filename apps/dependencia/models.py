from django.db import models

# Este modelo es padre de una dependencia
class Raiz(models.Model):
    opcionesRaiz = (
        ('s','Secretaría'),
        ('o','Otro')
    )
    nombre = models.CharField(max_length=100,blank=True, null=True)
    tipo = models.CharField(max_length=30,choices=opcionesRaiz)
    responsable = models.CharField(max_length=100,blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=5,default='A')
    def __str__(self):
        return self.nombre
    
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
    adscrita = models.OneToOneField(Raiz,blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    
class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    dependencia = models.ForeignKey(Dependencia,on_delete=models.CASCADE)
    encargado = models.CharField(max_length=100)
    def __str__(self):
        return self.dependencia.nombre + ', ' + self.nombre



