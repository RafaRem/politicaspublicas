# Generated by Django 2.2 on 2019-06-07 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0015_auto_20190607_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programaoperativo',
            name='objetivo',
        ),
    ]
