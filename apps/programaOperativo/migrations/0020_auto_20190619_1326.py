# Generated by Django 2.2 on 2019-06-19 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0019_actividad_observaciones'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='acciones',
            options={'verbose_name': 'Acción de programa operativo', 'verbose_name_plural': 'Acciones de programas operativos'},
        ),
        migrations.AlterModelOptions(
            name='actividad',
            options={'verbose_name': 'Actividad', 'verbose_name_plural': 'Actividades'},
        ),
        migrations.AlterModelOptions(
            name='detallesgasto',
            options={'verbose_name': 'Detalle de gasto por actividad', 'verbose_name_plural': 'Detalles de gasto por actividades'},
        ),
        migrations.AlterModelOptions(
            name='programaoperativo',
            options={'verbose_name': 'Programa operativo', 'verbose_name_plural': 'Programas operativos'},
        ),
    ]
