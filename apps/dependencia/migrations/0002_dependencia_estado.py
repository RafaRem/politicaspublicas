# Generated by Django 2.2 on 2019-06-04 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dependencia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependencia',
            name='estado',
            field=models.CharField(choices=[('a', 'Acticho'), ('i', 'Inactivo')], default='a', max_length=30),
        ),
    ]
