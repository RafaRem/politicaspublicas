# Generated by Django 2.2 on 2019-08-13 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0017_periodogobierno_permitircambios'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meta',
            name='cualitativa',
        ),
        migrations.AlterField(
            model_name='meta',
            name='descripcion',
            field=models.CharField(max_length=300, verbose_name='Descripción de la meta'),
        ),
    ]
