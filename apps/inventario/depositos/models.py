from audioop import reverse
from django.db import models
from datetime import datetime

# Create your models here.
class Deposito(models.Model):
    """
    Clase que define la estructura de un deposito
    """
    descripcion = models.CharField(max_length = 200, help_text = "Ingrese descripcion del deposito")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)

    class Mwta:
        verbose_name = "Deposito"
        verbose_name_plural = "Depositos"
        default_permissions =  ()
        permissions = (
            ('add_deposito', 'Agregar Deposito'),
            ('change_deposito', 'Editar Deposito'),
            ('delete_deposito', 'Eliminar Deposito'),
            ('view_deposito', 'Listar Depositos'))

    def __str__(self):
        """Formato de la ciudad"""
        return '{0}'.format(self.descripcion)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un deposito en particular."""
        return reverse('deposito-detail', args=[str(self.id)])
