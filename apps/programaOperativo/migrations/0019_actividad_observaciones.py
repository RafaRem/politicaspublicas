# Generated by Django 2.2 on 2019-06-19 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0018_auto_20190617_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='observaciones',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
    ]