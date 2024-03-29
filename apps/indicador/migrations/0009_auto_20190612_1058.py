# Generated by Django 2.2 on 2019-06-12 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dependencia', '0003_auto_20190604_1415'),
        ('indicador', '0008_sectoreconomico'),
    ]

    operations = [
        migrations.AddField(
            model_name='conceptogasto',
            name='dependencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dependencia.Dependencia', verbose_name='Dependencia a la que pertenece'),
        ),
        migrations.AddField(
            model_name='conceptogasto',
            name='tipoDependencia',
            field=models.CharField(choices=[('d', 'Dependencia'), ('p', 'Paramunicipal')], default='d', max_length=30),
        ),
    ]
