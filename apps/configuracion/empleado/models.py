from django.db import models
from apps.configuracion.servicio.models import Servicio

# Create your models here.
class Empleado(models.Model):
    nombre_emp = models.CharField(max_length=200)
    apellido_emp = models.CharField(max_length=200)
    ci_empe = models.CharField(max_length=200)
    disponible = models.BooleanField(blank=True, null=True, default=True)
    emp_disponible_reserva = models.CharField(max_length=200, blank=True, null=True, default="S")    
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=200, blank=True, null=True, default="S")
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        default_permissions =  ()
        permissions = (
            ('add_empleado', 'Agregar Empleado'),
            ('change_empleado', 'Editar Empleado'),
            ('delete_empleado', 'Eliminar Empleado'),
            ('view_empleado', 'Listar Empleados')) 

    def __str__(self):
        """Formato del empleado"""
        return '{0}'.format(self.nombre_emp)