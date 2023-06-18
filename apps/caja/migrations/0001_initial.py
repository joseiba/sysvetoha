# Generated by Django 4.1.7 on 2023-06-18 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_alta', models.CharField(default='18/06/2023 17:54:45 hs', max_length=500, null=True)),
                ('fecha_alta', models.CharField(default='18/06/2023', max_length=500, null=True)),
                ('fecha_cierre', models.CharField(default='-', max_length=500, null=True)),
                ('total_pos', models.FloatField(blank=True, default=0, max_length=1000, null=True)),
                ('total_pos_formateado', models.CharField(max_length=800, null=True)),
                ('total_efectivo', models.FloatField(blank=True, default=0, max_length=1000, null=True)),
                ('total_efectivo_formateado', models.CharField(max_length=800, null=True)),
                ('saldo_inicial', models.FloatField(blank=True, max_length=800, null=True)),
                ('saldo_inicial_formateado', models.CharField(max_length=800, null=True)),
                ('total_ingreso', models.FloatField(blank=True, default=0, max_length=1000, null=True)),
                ('total_ingreso_formateado', models.CharField(max_length=800, null=True)),
                ('total_egreso', models.FloatField(blank=True, default=0, max_length=1000, null=True)),
                ('total_egreso_formateado', models.CharField(max_length=800, null=True)),
                ('total_dia', models.FloatField(blank=True, default=0, max_length=1000, null=True)),
                ('saldo_a_entregar', models.FloatField(blank=True, default=0, max_length=1000, null=True)),
                ('saldo_a_entregar_formateado', models.CharField(max_length=800, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('apertura_cierre', models.CharField(blank=True, default='A', max_length=2, null=True)),
            ],
            options={
                'permissions': (('add_caja', 'Agregar Caja'), ('change_caja', 'Cierre Caja'), ('delete_caja', 'Eliminar Caja'), ('view_caja', 'Listar Cajas')),
                'default_permissions': (),
            },
        ),
    ]
