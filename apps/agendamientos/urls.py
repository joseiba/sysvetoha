from django.urls import path

from apps.configuracion.servicio.views import list_servicio, add_servicio, edit_servicio
from .views import (add_reserva, edit_reserva, list_reserva, delete_reserva, search_reserva, 
validar_fecha_hora, get_mascota_cliente, get_min_service, get_mascota_selected)

urlpatterns = [
    path('listServicio/', list_servicio , name="list_servicio"),
    path('addServicio/',  add_servicio, name="add_servicio"),
    path('editServicio/<int:id>/',edit_servicio , name="edit_servicio"),
    # path('reserva/searchServicio/', search_servicio, name="search_servicio"),
    # path('reserva/bajaServicio/<int:id>/', delete_servicio, name="delete_servicio"),
    path('listReserva/', list_reserva , name="list_reserva"),
    path('addReserva/',  add_reserva, name="add_reserva"),
    path('editReserva/<int:id>/',edit_reserva , name="edit_reserva"),
    path('bajaReserva/<int:id>/', delete_reserva, name="delete_reserva"),
    path('searchReserva/', search_reserva, name="search_reserva"),
    path('validarDatos/', validar_fecha_hora, name="search_reserva"),
    path('getMascotaCliente', get_mascota_cliente, name="get_mascota_cliente"),
    path('getTimeServices', get_min_service, name="get_min_service"),
    path('getMascotaSelected', get_mascota_selected, name="get_mascota_selected"),
]