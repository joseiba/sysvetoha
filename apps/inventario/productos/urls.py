from django.urls import path
from apps.inventario.productos.views import (add_producto,edit_producto,list_producto_general_ajax,
list_productos_general,list_tipo_producto,get_list_tipo_producto,add_tipo_producto,alta_tipo_producto,
edit_tipo_producto,baja_tipo_producto,vence_si_no, add_tipo_producto_from_producto)

urlpatterns = [
    #Urls tipo producto
    path('tipoProducto/add/',add_tipo_producto , name="add_tipo_producto"),
    path('tipoProducto/list/', list_tipo_producto, name="list_tipo_producto"),
    path('tipoProducto/edit/<int:id>/', edit_tipo_producto, name="edit_tipo_producto"),
    path('tipoProducto/baja/<int:id>/', baja_tipo_producto, name="baja_tipo_producto"),
    path('tipoProducto/alta/<int:id>/', alta_tipo_producto, name="alta_tipo_producto"),
    path('tipoProducto/vence_si_no/', vence_si_no, name="vence_si_no"),
    path('tipoProducto/get_list_tipo_producto/', get_list_tipo_producto, name="get_list_tipo_producto"),

    #Urls productos
    path('add/', add_producto, name="add_producto"),
    path('list/', list_productos_general, name="list_productos_general"),
    path('list_general_ajax/', list_producto_general_ajax, name="list_producto_general_ajax"),
    path('edit/<int:id>/', edit_producto, name="edit_producto"),
    path('add/tipoProducto/', add_tipo_producto_from_producto, name="add_tipo_producto_from_producto"),   
]