from django.db import models

from datetime import datetime


# Create your models here.
date = datetime.now()
class Caja(models.Model):
    """
    Clase que define la estructura de caja
    """

    fecha_hora_alta = models.CharField(max_length=500, default = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S hs"), null=True)
    fecha_alta = models.CharField(max_length=500, default = datetime.strftime(datetime.now() , "%d/%m/%Y"), null=True)
    fecha_cierre = models.CharField(max_length=500, default = "-", null=True)
    total_pos = models.FloatField(max_length=1000, null=True, blank=True, default=0)
    total_pos_formateado = models.CharField(max_length=800, null=True)
    total_efectivo = models.FloatField(max_length=1000, null=True, blank=True, default=0)
    total_efectivo_formateado = models.CharField(max_length=800, null=True)
    saldo_inicial = models.FloatField(max_length=800, null=True, blank=True)
    saldo_inicial_formateado = models.CharField(max_length=800, null=True)
    total_ingreso = models.FloatField(max_length=1000, null=True, blank=True, default=0)
    total_ingreso_formateado = models.CharField(max_length=800, null=True)
    total_egreso = models.FloatField(max_length=1000, null=True, blank=True, default=0)
    total_egreso_formateado = models.CharField(max_length=800, null=True)
    total_dia = models.FloatField(max_length=1000, null=True, blank=True, default=0)
    saldo_a_entregar = models.FloatField(max_length=1000, null=True, blank=True, default=0)
    saldo_a_entregar_formateado = models.CharField(max_length=800, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    apertura_cierre = models.CharField(max_length=2, default="A", blank=True, null=True)        

    class Meta:
        default_permissions =  ()
        permissions = (
            ('add_caja', 'Agregar Caja'),
            ('change_caja', 'Cierre Caja'),
            ('delete_caja', 'Eliminar Caja'),
            ('view_caja', 'Listar Cajas'))     
