from django.db import models

from datetime import datetime


# Create your models here.
date = datetime.now()
class Proveedor(models.Model):
    """[summary]

    Args:
        models ([Proveedor]): [Contiene la informacion de los proveedores]
    """    
    nombre_proveedor = models.CharField(max_length=500, help_text="Ingrese nombre del proveedor")
    direccion = models.CharField(max_length=500, help_text="Ingrese la direccion")
    ruc_proveedor = models.CharField(max_length=500, default="-", help_text="Ingrese el ruc del proveedor")
    telefono = models.CharField(max_length = 500, help_text="Ingrese el telefono del proveedor")
    email = models.EmailField(max_length = 500, help_text = "Ingrese email del proveedor", null=True, blank=True, default="-")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        default_permissions =  ()
        permissions = (
            ('add_proveedor', 'Agregar Proveedor'),
            ('change_proveedor', 'Editar Proveedor'),
            ('delete_proveedor', 'Eliminar Proveedor'),
            ('view_proveedor', 'Listar Proveedores'))


    def __str__(self):
        return  'Proveedor: %s - ruc: %s' % (self.nombre_proveedor, self.ruc_proveedor)