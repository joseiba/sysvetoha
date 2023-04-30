from django.db import models

from apps.inventario.productos.models import Producto

class TipoVacuna(models.Model):

    opciones = (
        ('S', 'Si'),
        ('N', 'No'),
    )
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False)
    nombre_vacuna =  models.CharField(max_length = 500, blank=True, null=True)
    periodo_aplicacion = models.CharField(max_length = 500, blank=True, null=True)
    multi_aplicaciones = models.CharField(max_length=2, choices=opciones, default="N", blank=True, null=True)
    class Meta:
        verbose_name = "Vacunas"
        verbose_name_plural = "Vacunas"
        default_permissions =  ()
        permissions = (
            ('add_tipovacuna', 'Agregar Vacuna'),
            ('change_tipovacuna', 'Editar Vacuna'),
            ('delete_tipovacuna', 'Eliminar Vacuna'),
            ('view_tipovacuna', 'Listar Vacunas')) 

    def __str__(self):
        """Formato de la vacuna"""
        return '{0}'.format(self.nombre_vacuna)    