# Generated by Django 2.2 on 2019-06-06 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0005_auto_20190606_1726'),
        ('programaOperativo', '0011_auto_20190605_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acciones',
            name='poblacionObjetivo',
        ),
        migrations.AddField(
            model_name='acciones',
            name='categoriaPoblacion',
            field=models.ManyToManyField(blank=True, to='indicador.CategoriaPoblacion'),
        ),
        migrations.AddField(
            model_name='acciones',
            name='escolaridad',
            field=models.ManyToManyField(blank=True, to='indicador.Escolaridad'),
        ),
        migrations.AddField(
            model_name='acciones',
            name='gruposVulnerables',
            field=models.ManyToManyField(blank=True, to='indicador.GruposVulnerables'),
        ),
        migrations.AddField(
            model_name='acciones',
            name='sectorSocial',
            field=models.ManyToManyField(blank=True, to='indicador.SectorSocial'),
        ),
        migrations.AddField(
            model_name='acciones',
            name='ubicacion',
            field=models.ManyToManyField(blank=True, to='indicador.Ubicacion'),
        ),
        migrations.AlterUniqueTogether(
            name='detallesgasto',
            unique_together={('actividad', 'gasto')},
        ),
    ]
