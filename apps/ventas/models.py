from django.db import models
from datetime import datetime

from apps.inventario.productos.models import Producto
from apps.configuracion.servicio.models import Servicio
from apps.cliente.models import Cliente
from apps.caja.models import Caja
date = datetime.now()
# Create your models here.

ESTADOS_FACTURA = [
    ('PENDIENTE', 'Pendiente'),
    ('CANCELADO', 'Cancelado'),
    ('FINALIZADO', 'Finalizado'),
]   


class CabeceraVenta(models.Model):
    nro_timbrado = models.CharField(max_length=500, null=True)
    nro_factura = models.CharField(max_length=500, null=True)
    fecha_inicio_timbrado = models.CharField(max_length=500, null=True)
    fecha_fin_timbrado = models.CharField(max_length=500, null=True)
    ruc_empresa = models.CharField(max_length=500, null=True)
    fecha_emision = models.CharField(max_length=500, default = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S hs"), null=True)
    fecha_alta = models.CharField(max_length=500, default = date.strftime("%d/%m/%Y"), null=True)
    tipo_factura = models.BooleanField(default=True)
    contado_pos =  models.CharField(max_length=2, default="C", blank=True, null=True)
    estado = models.CharField(max_length=500, choices=ESTADOS_FACTURA, default=ESTADOS_FACTURA[0])
    total_iva = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    total_formateado = models.CharField(max_length=800, blank=True, null=True)
    factura_cargada = models.CharField(max_length=2, default="N", blank=True, null=True)
    factura_anulada = models.CharField(max_length=2, default="N", blank=True, null=True)
    factura_caja = models.CharField(max_length=2, default="N", blank=True, null=True) 
    factura_to_reporte = models.CharField(max_length=2, default="N", blank=True, null=True)
    factura_reporte_cantidad_mes = models.CharField(max_length=2, default="N", blank=True, null=True)
    factura_servicio_reporte = models.CharField(max_length=2, default="N", blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    id_caja = models.ForeignKey(Caja, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'Factura Venta: %s - Cliente: %s' % (self.nro_factura, self.id_cliente)

    class Meta:
        verbose_name = 'Factura Venta'
        verbose_name_plural = 'Facturas Ventas'
        default_permissions =  ()
        permissions = (
            ('add_cabeceraventa', 'Agregar Venta'),
            ('change_cabeceraventa', 'Editar Venta'),
            ('delete_cabeceraventa', 'Anular Venta'),
            ('view_cabeceraventa', 'Listar Facturas Ventas'))          

class DetalleVenta(models.Model):
    id_factura_venta = models.ForeignKey('CabeceraVenta', on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.IntegerField()
    detalle_cargado_reporte = models.CharField(max_length=2, default="N", blank=True, null=True)
    detalle_cargado_mes = models.CharField(max_length=2, default="N", blank=True, null=True)
    subtotal = models.CharField(max_length=900, blank=True, null=True)
    detalle_cargado_servicio = models.CharField(max_length=2, default="N", blank=True, null=True)
    descripcion = models.CharField(max_length=800, blank=True)
    

    class Meta:
        ordering = ['id']    