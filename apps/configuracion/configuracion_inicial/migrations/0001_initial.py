# Generated by Django 4.0.4 on 2022-10-06 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apertura_caja_inicial', models.CharField(blank=True, max_length=200, null=True)),
                ('ubicacion_deposito_inicial', models.CharField(blank=True, max_length=200, null=True)),
                ('nombre_empresa', models.CharField(blank=True, max_length=500, null=True)),
                ('direccion', models.CharField(blank=True, max_length=500, null=True)),
                ('cuidad', models.CharField(blank=True, max_length=500, null=True)),
                ('telefono', models.CharField(blank=True, max_length=500, null=True)),
                ('nro_timbrado', models.CharField(blank=True, max_length=500, null=True)),
                ('fecha_inicio_timbrado', models.CharField(blank=True, max_length=500, null=True)),
                ('fecha_fin_timbrado', models.CharField(blank=True, max_length=500, null=True)),
                ('ruc_empresa', models.CharField(blank=True, max_length=500, null=True)),
                ('dias_a_vencer', models.IntegerField(blank=True, default=30, null=True)),
                ('dias_alert_vacunas', models.IntegerField(blank=True, default=30, null=True)),
            ],
            options={
                'verbose_name': 'Configuracion Empresa',
                'verbose_name_plural': 'Configuraciones Empresas',
                'permissions': (('add_confiempresa', 'Agregar Configuracion'), ('change_confiempresa', 'Editar Configuracion'), ('delete_confiempresa', 'Eliminar Configuracion'), ('view_confiempresa', 'Listar Configuraciones')),
                'default_permissions': (),
            },
        ),
    ]
