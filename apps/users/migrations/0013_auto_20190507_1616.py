# Generated by Django 2.2 on 2019-05-07 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20190507_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='created',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='dependencia',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='modified',
        ),
        migrations.AlterField(
            model_name='persona',
            name='edad',
            field=models.IntegerField(blank=True, max_length=30),
        ),
    ]
