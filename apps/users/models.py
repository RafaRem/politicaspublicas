from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def definirCadena(self):
        cadena = ""
        return cadena.format()
    def __str__(self):
        return self.definirCadena()


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
    edad = models.IntegerField(max_length=30, blank=True)   