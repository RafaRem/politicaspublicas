# Generated by Django 2.2 on 2019-06-04 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objetivo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objetivo',
            name='estado',
            field=models.CharField(choices=[('a', 'Activo'), ('a', 'Inactivo')], default='a', max_length=3),
        ),
    ]
