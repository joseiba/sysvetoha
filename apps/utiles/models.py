from django.db import models
from datetime import datetime

from apps.inventario.productos.models import Producto

date = datetime.now()
# Create your models here.
class Timbrado(models.Model): 
    nro_timbrado = models.CharField(max_length=500, null=True, blank=True)
    fecha_inicio_timbrado = models.CharField(max_length=500, null=True, blank=True)
    fecha_fin_timbrado = models.CharField(max_length=500, null=True, blank=True)
    vencido = models.CharField(max_length=2, default="N", blank=True, null=True)

    def __str__(self):
        return  'Timbrado: ' % (self.nro_timbrado)
    

class VacunasAplicadas(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    cantidad_aplicadas = models.FloatField(null=True, blank=True, default=0)
    date = models.DateField(auto_now=False, null=True, blank=True)


class ServicioVendido(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    cantidad_vendida_total = models.FloatField(null=True, blank=True, default=0)
    date = models.DateField(auto_now=False, null=True, blank=True)

class ProductoVendido(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    cantidad_vendida_total = models.FloatField(null=True, blank=True, default=0)


class ProductoVendidoMes(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=False, null=True, blank=True)    
    cantidad_vendida_total = models.FloatField(null=True, blank=True, default=0)