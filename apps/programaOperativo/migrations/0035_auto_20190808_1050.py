# Generated by Django 2.2 on 2019-08-08 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programaOperativo', '0034_auto_20190729_0856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acciones',
            name='descripcionMeta',
        ),
        migrations.AlterField(
            model_name='acciones',
            name='meta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='indicador.Meta'),
        ),
    ]