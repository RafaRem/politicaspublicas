# Generated by Django 2.2 on 2019-07-10 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objetivo', '0004_auto_20190619_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objetivo',
            name='estado',
            field=models.CharField(choices=[('a', 'Activo'), ('i', 'Inactivo')], default='a', max_length=3),
        ),
    ]
