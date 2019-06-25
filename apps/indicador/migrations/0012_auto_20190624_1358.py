# Generated by Django 2.2 on 2019-06-24 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0011_periodo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='periodo',
            options={'verbose_name': 'Periodo', 'verbose_name_plural': 'Periodos'},
        ),
        migrations.AddField(
            model_name='periodo',
            name='capturaHabilitada',
            field=models.BooleanField(default=True, verbose_name='Captura habilitada'),
        ),
    ]
