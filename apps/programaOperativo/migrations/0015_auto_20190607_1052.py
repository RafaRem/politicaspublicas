# Generated by Django 2.2 on 2019-06-07 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0014_remove_actividad_presupuestoejercido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programaoperativo',
            name='beneficiarios',
        ),
        migrations.RemoveField(
            model_name='programaoperativo',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='programaoperativo',
            name='estrategias',
        ),
        migrations.RemoveField(
            model_name='programaoperativo',
            name='justificacion',
        ),
        migrations.RemoveField(
            model_name='programaoperativo',
            name='objetivos',
        ),
        migrations.RemoveField(
            model_name='programaoperativo',
            name='problematicaSocial',
        ),
        migrations.RemoveField(
            model_name='programaoperativo',
            name='tipoPrograma',
        ),
    ]
