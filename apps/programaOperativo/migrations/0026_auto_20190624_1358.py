# Generated by Django 2.2 on 2019-06-24 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0025_auto_20190621_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='estado',
            field=models.CharField(choices=[('p', 'Programada'), ('t', 'Por revisar'), ('i', 'Inactiva'), ('r', 'Válida'), ('n', 'No válida')], default='p', max_length=30),
        ),
    ]
