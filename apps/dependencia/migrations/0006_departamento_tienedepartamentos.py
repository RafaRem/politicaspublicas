# Generated by Django 2.2 on 2019-08-11 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dependencia', '0005_auto_20190724_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='departamento',
            name='tieneDepartamentos',
            field=models.BooleanField(default=True, verbose_name='¿Tiene departamentos?'),
        ),
    ]
