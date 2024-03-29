# Generated by Django 2.2 on 2019-10-15 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dependencia', '0008_auto_20191015_1334'),
        ('programaOperativo', '0048_auto_20191015_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeneficiariosActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='programaOperativo.Actividad')),
                ('alcance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dependencia.Alcance')),
            ],
            options={
                'verbose_name': 'Cantidad de beneficiarios por actividad',
                'unique_together': {('alcance', 'actividad')},
            },
        ),
    ]
