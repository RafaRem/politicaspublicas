# Generated by Django 2.2 on 2019-08-09 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0015_auto_20190809_1100'),
        ('programaOperativo', '0036_auto_20190808_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='acciones',
            name='indicador',
            field=models.ManyToManyField(blank=True, to='indicador.Indicador'),
        ),
        migrations.CreateModel(
            name='GastoAnualAsignado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField(verbose_name='Cantidad asignada')),
                ('periodoGobierno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='indicador.PeriodoGobierno', verbose_name='Gasto asignado al periodo')),
                ('programaOperativo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='programaOperativo.ProgramaOperativo', verbose_name='Programa operativo')),
            ],
            options={
                'verbose_name': 'Gasto anual asignado',
                'verbose_name_plural': 'Gastos anuales asignados',
            },
        ),
    ]