# Generated by Django 2.2 on 2019-06-04 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dependencia', '0002_dependencia_estado'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departamento',
            options={'verbose_name': 'Departamentos'},
        ),
        migrations.AlterModelOptions(
            name='dependencia',
            options={'verbose_name': 'Dependencias'},
        ),
        migrations.AlterModelOptions(
            name='raiz',
            options={'verbose_name': 'Secretarías/Direcciones Generales'},
        ),
    ]