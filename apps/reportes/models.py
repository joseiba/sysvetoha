from django.db import models

# Create your models here.
class Reporte(models.Model):
    cantidad_reporte = models.IntegerField(default=0)

    class Mwta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
        default_permissions =  ()
        permissions = (
            ('add_reporte', 'Agregar Reporte'),
            ('change_reporte', 'Editar Reporte'),
            ('delete_reporte', 'Eliminar Reporte'),
            ('view_reporte', 'Ver Reportes')) 