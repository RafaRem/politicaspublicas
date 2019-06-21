# Generated by Django 2.2 on 2019-06-21 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0011_periodo'),
        ('programaOperativo', '0023_remove_actividad_presupuestoprogramado'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallesgasto',
            name='periodo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='indicador.Periodo', verbose_name='Periodo del gasto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='detallesgasto',
            name='accion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='programaOperativo.Acciones', verbose_name='Acción'),
        ),
        migrations.AlterField(
            model_name='detallesgasto',
            name='cantidad',
            field=models.CharField(max_length=100, verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='detallesgasto',
            name='gasto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='indicador.ConceptoGasto', verbose_name='Concepto de gasto'),
        ),
    ]