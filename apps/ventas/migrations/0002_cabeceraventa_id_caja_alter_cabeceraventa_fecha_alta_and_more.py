# Generated by Django 4.1.7 on 2023-06-24 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0003_alter_caja_fecha_alta_alter_caja_fecha_hora_alta'),
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabeceraventa',
            name='id_caja',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='caja.caja'),
        ),
        migrations.AlterField(
            model_name='cabeceraventa',
            name='fecha_alta',
            field=models.CharField(default='24/06/2023', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='cabeceraventa',
            name='fecha_emision',
            field=models.CharField(default='24/06/2023 12:27:51 hs', max_length=500, null=True),
        ),
    ]
