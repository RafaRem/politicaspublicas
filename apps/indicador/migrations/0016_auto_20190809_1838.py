# Generated by Django 2.2 on 2019-08-10 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0015_auto_20190809_1100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='periodogobierno',
            old_name='fehcaInicial',
            new_name='fechaInicial',
        ),
    ]
