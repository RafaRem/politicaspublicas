# Generated by Django 2.2 on 2019-06-20 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0022_remove_detallesgasto_actividad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actividad',
            name='presupuestoProgramado',
        ),
    ]
