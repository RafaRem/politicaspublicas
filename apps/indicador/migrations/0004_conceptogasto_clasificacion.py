# Generated by Django 2.2 on 2019-06-05 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0003_clasificaciongasto'),
    ]

    operations = [
        migrations.AddField(
            model_name='conceptogasto',
            name='clasificacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='indicador.ClasificacionGasto', verbose_name='Clasificación del gasto'),
            preserve_default=False,
        ),
    ]
