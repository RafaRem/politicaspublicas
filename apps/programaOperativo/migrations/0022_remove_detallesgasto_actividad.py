# Generated by Django 2.2 on 2019-06-20 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0021_auto_20190620_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallesgasto',
            name='actividad',
        ),
    ]
