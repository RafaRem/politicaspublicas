# Generated by Django 2.2 on 2019-10-15 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_delete_logactividad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tipoUsuario',
            field=models.CharField(choices=[('s', 'Super usuario'), ('a', 'Administrador'), ('e', 'Enlace'), ('i', 'Analista')], max_length=30, verbose_name='Tipo de usuario'),
        ),
    ]