from audioop import reverse
from django.db import models

# Create your models here.
class Servicio(models.Model):
    """
    Clase que define la estructura de un Servicio
    """
    nombre_servicio = models.CharField(max_length = 200, help_text = "Ingrese nombre del servicio")
    precio_servicio = models.CharField(max_length = 200, help_text = "Ingrese el precio del servicio")
    min_serv = models.CharField(max_length = 200)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=200, blank=True, null=True, default="S")


    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        default_permissions =  ()
        permissions = (
            ('add_servicio', 'Agregar Servicio'),
            ('change_servicio', 'Editar Servicio'),
            ('delete_servicio', 'Eliminar Servicio'),
            ('view_servicio', 'Listar Servicios'))         

    def __str__(self):
        """Formato del servicio"""
        return '{0}'.format(self.nombre_servicio)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de una Servicio en particular."""
        return reverse('servicio-detail', args=[str(self.id)])

    def obtener_dict(self):
        dict = {}
        dict['codigo_producto'] = self.id
        dict['nombre'] = self.nombre_servicio
        dict['description'] = self.nombre_servicio
        dict['precio'] = self.precio_servicio
        dict['tipo'] = 'S'
        return dict