from audioop import reverse
from django.db import models
from datetime import datetime

from apps.inventario.depositos.models import Deposito

# Create your models here.
date = datetime.now()
class TipoProducto(models.Model):
    """
    Clase que define la estructura de un tipo de producto
    """
    opciones = (
        ('S', 'Si'),
        ('N', 'No'),
    )

    nombre_tipo = models.CharField(max_length = 200, help_text = "Ingrese nombre del tipo de producto")
    fecha_alta = models.CharField(max_length = 200, default = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S hs"), editable = False)
    fecha_baja = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    vence = models.CharField(max_length=2, choices=opciones, default="S", blank=True, null=True, help_text='El producto vence?')
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)

    class Mwta:
        verbose_name = "Tipo Producto"
        verbose_name_plural = "Tipo Productos"
        default_permissions =  ()
        permissions = (
            ('add_tipoproducto', 'Agregar Tipo Producto'),
            ('change_tipoproducto', 'Editar Tipo Producto'),
            ('delete_tipoproducto', 'Eliminar Tipo Producto'),
            ('view_tipoproducto', 'Listar Tipo Productos'))

    def __str__(self):
        """Formato del tipo producto"""
        return '{0}'.format(self.nombre_tipo)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un tipo de producto en particular."""
        return reverse('tipoProducto-detail', args=[str(self.id)])


class Producto(models.Model):
    """
    Clase que define la estructura de un producto
    """
    opciones = (
        ('1', '5%'),
        ('2', '10%'),
    )
    nombre_producto = models.CharField(max_length = 500, help_text = "Ingrese nombre del producto")
    descripcion = models.CharField(max_length = 500, help_text = "Ingrese descripcion del producto")
    fecha_vencimiento = models.CharField(max_length = 200,null = True, blank = True)
    fecha_baja = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    #fecha_movimiento = models.CharField(max_length = 200, null = True, blank = True)
    tipo_producto = models.ForeignKey('TipoProducto', on_delete=models.CASCADE, null=True)
    #fecha_compra = models.CharField(max_length = 200, default = date.strftime("%d/%m/%Y"), editable = False)
    precio_compra = models.CharField(max_length = 500,help_text = 'Ingrese precio de compra', blank=True, null=True, default="0")
    precio_venta = models.CharField(max_length = 500, help_text = 'Ingrese precio de venta')
    stock_minimo = models.IntegerField(help_text = 'Ingrese stock minimo')
    lote = models.CharField(max_length = 200, null = True, blank = True)
    stock = models.IntegerField(help_text = 'Ingrese stock minimo')
    iva = models.CharField(max_length=5, choices=opciones, help_text='Debe seleccionar el iva')
    #stock_total = models.IntegerField(null=True, blank=True)
    #stock_movido = models.IntegerField(blank = True, null=True, default=0)
    #servicio_o_producto = models.CharField(max_length=2, default="P", blank=True, null=True)
    #producto_vencido = models.CharField(max_length=2, default="N", blank=True, null=True)
    #id_servicio = models.IntegerField(blank = True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    #id_deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE, null=True)

    
    class Mwta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        default_permissions =  ()
        permissions = (
            ('add_producto', 'Agregar Producto'),
            ('change_producto', 'Editar Producto'),
            ('delete_producto', 'Eliminar Producto'),
            ('view_producto', 'Listar Productos')) 

    def __str__(self):
        """Formato del producto"""
        return '{0}'.format(self.nombre_producto)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un producto en particular."""
        return reverse('producto-detail', args=[str(self.id)])

    def obtener_dict(self):
        dict = {}
        dict['codigo_producto'] = self.id
        dict['nombre'] = self.nombre_producto
        dict['description'] = self.descripcion
        dict['precio'] = self.precio_venta
        dict['precio_compra'] = self.precio_compra
        dict['stock_sistema'] = self.stock
        #dict['tipo'] = self.servicio_o_producto
        return dict        