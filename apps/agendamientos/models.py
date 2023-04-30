from django.db import models
from django.urls import reverse

from apps.cliente.models import Cliente
from apps.mascotas.models import Mascota
from apps.configuracion.empleado.models import Empleado
from apps.configuracion.servicio.models import Servicio


class Reserva(models.Model):
    """
    Clase que define la estructura de la reserva
    """
    FINALIZADO = 'FIN'
    CANCELADO = 'CAN' 
    PENDIENTE = 'PEN'   
    estados =((FINALIZADO, 'Finalizado'),
                (CANCELADO, 'Cancelado'),
                (PENDIENTE, 'Pendiente'))
    descripcion = models.CharField(max_length=200, help_text = "Ingrese la descripción del la reserva", blank=True, null=True, default="-")
    fecha_reserva = models.DateField()
    hora_reserva = models.CharField(max_length=200)
    disponible_emp = models.CharField(max_length=2, default="S", blank=True, null=True)
    estado_re = models.CharField(max_length=15, choices=estados, default=PENDIENTE, help_text="Seleccione el estado", blank=True, null=True)
    color_estado = models.CharField(max_length=200, blank=True, null=True, default="light blue")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=False)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False)
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, null=False)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        default_permissions =  ()
        permissions = (
            ('add_reserva', 'Agregar Reserva'),
            ('change_reserva', 'Editar Reserva'),
            ('delete_reserva', 'Eliminar Reserva'),
            ('view_reserva', 'Listar Reservas'))         

    def __str__(self):
        """Formato de reserva"""
        return '{0}'.format(self.id_mascota.nombre_mascota)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de una reserva en particular."""
        return reverse('reserva-detail', args=[str(self.id)])
