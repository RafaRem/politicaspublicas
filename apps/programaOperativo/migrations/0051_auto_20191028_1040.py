# Generated by Django 2.2 on 2019-10-28 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0022_unidadmedida_variable'),
        ('programaOperativo', '0050_metaaccion'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='metaaccion',
            unique_together={('accion', 'variable', 'periodoGobierno')},
        ),
    ]
