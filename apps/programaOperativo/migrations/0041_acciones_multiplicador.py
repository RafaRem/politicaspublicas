# Generated by Django 2.2 on 2019-08-13 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0040_auto_20190813_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='acciones',
            name='multiplicador',
            field=models.IntegerField(default=1),
        ),
    ]
