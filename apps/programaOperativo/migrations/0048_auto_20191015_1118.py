# Generated by Django 2.2 on 2019-10-15 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0047_auto_20191015_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='beneficiarios',
            field=models.CharField(blank=True, default='0', max_length=10, null=True, verbose_name='Número de beneficiarios/Asistentes'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='descripcion',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Descripción breve'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='nombre',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Actividad'),
        ),
    ]
