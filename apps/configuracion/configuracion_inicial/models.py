from django.db import models
from datetime import date, datetime, timedelta


# Create your models here.
class ConfiEmpresa(models.Model):
    """
    Clase que define la la configuracion de la empresa
    """
    apertura_caja_inicial = models.CharField(max_length=200, blank=True, null=True)
    ubicacion_deposito_inicial =  models.CharField(max_length=200, blank=True, null=True)
    nombre_empresa = models.CharField(max_length=500, blank=True, null=True)
    direccion = models.CharField(max_length=500, blank=True, null=True)
    cuidad = models.CharField(max_length=500, blank=True, null=True)
    telefono = models.CharField(max_length=500, blank=True, null=True)
    nro_timbrado =  models.CharField(max_length=500, blank=True, null=True)
    fecha_inicio_timbrado = models.CharField(max_length=500, blank=True, null=True)
    fecha_fin_timbrado = models.CharField(max_length=500, blank=True, null=True)
    ruc_empresa = models.CharField(max_length=500, blank=True, null=True)
    dias_a_vencer = models.IntegerField(blank=True, null=True, default=30)
    dias_alert_vacunas = models.IntegerField(blank=True, null=True, default=30)
    class Meta:
        verbose_name = "Configuracion Empresa"
        verbose_name_plural = "Configuraciones Empresas"
        default_permissions =  ()
        permissions = (
            ('add_confiempresa', 'Agregar Configuracion'),
            ('change_confiempresa', 'Editar Configuracion'),
            ('delete_confiempresa', 'Eliminar Configuracion'),
            ('view_confiempresa', 'Listar Configuraciones'))        

    def __str__(self):
        """Formato de configurcion"""
        return '{0}'.format(self.id)