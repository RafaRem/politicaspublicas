# Generated by Django 2.2 on 2019-06-07 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0007_categoriapoblacion_sexo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectorEconomico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Sectores económicos',
            },
        ),
    ]
