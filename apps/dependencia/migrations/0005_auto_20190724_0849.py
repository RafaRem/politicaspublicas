# Generated by Django 2.2 on 2019-07-24 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dependencia', '0004_auto_20190619_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependencia',
            name='estado',
            field=models.CharField(choices=[('a', 'Activo'), ('i', 'Inactivo')], default='a', max_length=30),
        ),
    ]
