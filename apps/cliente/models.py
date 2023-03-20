from audioop import reverse
from django.db import models

# Create your models here.
class Ciudad(models.Model):
    """
    Clase que define la estructura de una ciudad
    """
    nombre_ciudad = models.CharField(max_length = 200, help_text = "Ingrese nombre de la ciudad")
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        default_permissions =  ()
        permissions = (
            ('add_ciudad', 'Agregar Ciudad'),
            ('change_ciudad', 'Editar Ciudad'),
            ('delete_ciudad', 'Eliminar Ciudad'),
            ('view_ciudad', 'Listar Ciudades'))

    def __str__(self):
        """Formato de la ciudad"""
        return '{0}'.format(self.nombre_ciudad)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de una ciudad en particular."""
        return reverse('ciudad-detail', args=[str(self.id)])     

        
class Cliente(models.Model):
    """
    Clase que define la estructura de un cliente
    """

    nombre_cliente = models.CharField(max_length = 200, help_text = "Ingrese nombre del cliente")
    apellido_cliente = models.CharField(max_length = 200, help_text = "Ingrese apellido del cliente")
    direccion = models.CharField(max_length = 200, help_text = "Ingrese apellido del cliente")
    cedula = models.CharField(max_length = 200, help_text = "Ingrese cedula del cliente")
    ruc = models.CharField(max_length = 200, help_text = "Ingrese ruc del cliente", null=True, blank=True)
    telefono = models.CharField(max_length = 200, help_text = "Ingrese telefono del cliente")
    email = models.EmailField(max_length = 200, help_text = "Ingrese email del cliente", null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    id_ciudad = models.ForeignKey('Ciudad', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        """Formato del cliente"""
        if self.ruc == None:
            return 'Cliente: %s %s- cedula: %s' % (self.nombre_cliente, self.apellido_cliente, self.cedula)
        return  'Cliente: %s %s - ruc: %s' % (self.nombre_cliente, self.apellido_cliente, self.ruc)
        

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un cliente en particular."""
        return reverse('cliente-detail', args=[str(self.id)])
    class Meta:
        ordering = ['last_modified']
        default_permissions =  ()
        permissions = (
            ('add_cliente', 'Agregar Cliente'),
            ('change_cliente', 'Editar Cliente'),
            ('delete_cliente', 'Eliminar Cliente'),
            ('view_cliente', 'Listar Clientes')) 