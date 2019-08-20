# Generated by Django 2.2 on 2019-08-19 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0018_auto_20190813_1409'),
        ('programaOperativo', '0044_auto_20190819_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodoGobierno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='indicador.PeriodoGobierno', verbose_name='Periodo de gobierno a graficar')),
            ],
        ),
    ]
