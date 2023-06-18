# Generated by Django 4.1.7 on 2023-06-18 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0001_initial'),
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CabeceraVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro_timbrado', models.CharField(max_length=500, null=True)),
                ('nro_factura', models.CharField(max_length=500, null=True)),
                ('fecha_inicio_timbrado', models.CharField(max_length=500, null=True)),
                ('fecha_fin_timbrado', models.CharField(max_length=500, null=True)),
                ('ruc_empresa', models.CharField(max_length=500, null=True)),
                ('fecha_emision', models.CharField(default='18/06/2023 17:54:45 hs', max_length=500, null=True)),
                ('fecha_alta', models.CharField(default='18/06/2023', max_length=500, null=True)),
                ('tipo_factura', models.BooleanField(default=True)),
                ('contado_pos', models.CharField(blank=True, default='C', max_length=2, null=True)),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('CANCELADO', 'Cancelado'), ('FINALIZADO', 'Finalizado')], default=('PENDIENTE', 'Pendiente'), max_length=500)),
                ('total_iva', models.IntegerField(default=0)),
                ('total', models.FloatField(default=0)),
                ('total_formateado', models.CharField(blank=True, max_length=800, null=True)),
                ('factura_cargada', models.CharField(blank=True, default='N', max_length=2, null=True)),
                ('factura_anulada', models.CharField(blank=True, default='N', max_length=2, null=True)),
                ('factura_caja', models.CharField(blank=True, default='N', max_length=2, null=True)),
                ('factura_to_reporte', models.CharField(blank=True, default='N', max_length=2, null=True)),
                ('factura_reporte_cantidad_mes', models.CharField(blank=True, default='N', max_length=2, null=True)),
                ('factura_servicio_reporte', models.CharField(blank=True, default='N', max_length=2, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.CharField(blank=True, default='S', max_length=2, null=True)),
                ('id_cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cliente.cliente')),
            ],
            options={
                'verbose_name': 'Factura Venta',
                'verbose_name_plural': 'Facturas Ventas',
                'permissions': (('add_cabeceraventa', 'Agregar Venta'), ('change_cabeceraventa', 'Editar Venta'), ('delete_cabeceraventa', 'Anular Venta'), ('view_cabeceraventa', 'Listar Facturas Ventas')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, max_length=100, null=True)),
                ('cantidad', models.IntegerField()),
                ('detalle_cargado_reporte', models.CharField(blank=True, default='N', max_length=2, null=True)),
                ('detalle_cargado_mes', models.CharField(blank=True, default='N', max_length=2, null=True)),
                ('subtotal', models.CharField(blank=True, max_length=900, null=True)),
                ('detalle_cargado_servicio', models.CharField(blank=True, default='N', max_length=2, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=800)),
                ('id_factura_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.cabeceraventa')),
                ('id_producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
