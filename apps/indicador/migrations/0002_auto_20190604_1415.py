# Generated by Django 2.2 on 2019-06-04 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConceptoGasto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300, verbose_name='Nombre de gasto')),
            ],
            options={
                'verbose_name': 'Conceptos por gasto',
            },
        ),
        migrations.AlterModelOptions(
            name='categoriapoblacionobjetivo',
            options={'verbose_name': 'Categoría de población objetivo'},
        ),
        migrations.AlterModelOptions(
            name='poblacionobjetivo',
            options={'verbose_name': 'Población objetivo'},
        ),
    ]
