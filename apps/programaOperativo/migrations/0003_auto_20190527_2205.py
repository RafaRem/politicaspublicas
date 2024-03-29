# Generated by Django 2.2 on 2019-05-28 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0002_auto_20190527_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='estado',
            field=models.CharField(choices=[('p', 'Programada'), ('t', 'Terminada'), ('i', 'Inactiva'), ('r', 'Revisadad')], default='p', max_length=30),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='personasInvolucradas',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Personas involucradas'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='presupuestoEjercido',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Presupuesto ejercido'),
        ),
    ]
