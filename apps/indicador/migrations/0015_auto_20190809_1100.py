# Generated by Django 2.2 on 2019-08-09 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0014_auto_20190808_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('d', 'Desempeño'), ('g', 'Gestión')], max_length=30, verbose_name='Tipo de indicador')),
                ('nombre', models.CharField(max_length=300, verbose_name='Descripción del indicador')),
            ],
            options={
                'verbose_name': 'Indicador',
                'verbose_name_plural': 'Indicadores',
            },
        ),
        migrations.AlterField(
            model_name='meta',
            name='meta',
            field=models.IntegerField(verbose_name='Meta de número de actividades'),
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre de la variable')),
                ('cantidad', models.FloatField(verbose_name='Cantidad')),
                ('tipo', models.CharField(choices=[('p', 'Porcentual'), ('d', 'Divisor'), ('i', 'Dividendo'), ('t', 'Total')], max_length=30, verbose_name='Tipo de variable')),
                ('indicador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='indicador.Indicador', verbose_name='Indicador')),
            ],
            options={
                'verbose_name': 'Variable',
                'verbose_name_plural': 'Variables',
                'unique_together': {('indicador', 'tipo')},
            },
        ),
    ]