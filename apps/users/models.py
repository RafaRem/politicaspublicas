from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.dependencia.models import *
# Create your models here.

    #Proxy model que extiende el perfil de usuarios
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    types=(
        ('s', 'Super usuario'),
        ('a', 'Administrador'),
        ('e', 'Enlace'),
        ('i', 'Inspector')
    )
    dependencia = models.OneToOneField(Dependencia,blank=True, null=True, on_delete=models.PROTECT,verbose_name='Dependencia a la que pertenece')
    nombre = models.CharField(max_length=30, verbose_name='Nombre')
    apellido = models.CharField(max_length=30, verbose_name='Apellido(s)')
    telephone = models.CharField(max_length=30, blank=True, verbose_name='Teléfono')
    correo = models.EmailField(max_length=40,verbose_name='Correo electrónico')
    tipo = models.CharField(max_length=30,choices=types,verbose_name='Tipo de usuario')
    #The auto_now_add will set the timezone.now() only when the instance is created, 
    # and auto_now will update the field everytime the save method is called.
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Persona(models.Model):
    nombre = models.CharField(max_length=30)
    apellidopaterno= models.CharField(max_length=30, blank=True)
    apellidomaterno = models.CharField(max_length=30, blank=True)
    edad = models.IntegerField(blank=True)   
    
