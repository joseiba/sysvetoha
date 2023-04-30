from django.urls import path
from apps.inventario.productos.views import (add_producto,edit_producto,list_producto_general_ajax,
list_productos_general,list_tipo_producto,get_list_tipo_producto,add_tipo_producto,alta_tipo_producto,
edit_tipo_producto,baja_tipo_producto,vence_si_no, add_tipo_producto_from_producto, get_producto_antiparasitario,
list_producto, list_producto_vencido_ajax, mover_producto, search_producto, delete_producto, mover_producto_detalle_general,
list_ajuste_inventario_ajax,list_ajustar_inventario, add_ajuste_inventario, list_ajuste_inventario_historial_ajax,
list_ajustar_historial_inventario,get_producto_inventario, list_historico_producto,get_historico_producto)

urlpatterns = [
    #Urls tipo producto
    path('tipoProducto/add/',add_tipo_producto , name="add_tipo_producto"),
    path('tipoProducto/list/', list_tipo_producto, name="list_tipo_producto"),
    path('tipoProducto/edit/<int:id>/', edit_tipo_producto, name="edit_tipo_producto"),
    path('tipoProducto/baja/<int:id>/', baja_tipo_producto, name="baja_tipo_producto"),
    path('tipoProducto/alta/<int:id>/', alta_tipo_producto, name="alta_tipo_producto"),
    path('tipoProducto/vence_si_no/', vence_si_no, name="vence_si_no"),
    path('tipoProducto/get_list_tipo_producto/', get_list_tipo_producto, name="get_list_tipo_producto"),

    path('add/', add_producto, name="add_producto"),
    path('listDetalle/<int:id>/', list_producto, name="list_producto"),
    path('listGeneral/', list_productos_general, name="list_productos_general"),
    path('list_general_ajax/', list_producto_general_ajax, name="list_producto_general_ajax"),
    path('list_producto_vencido_ajax/', list_producto_vencido_ajax, name="list_producto_vencido_ajax"),
    path('edit/<int:id>/', edit_producto, name="edit_producto"),
    path('mover/<int:id>/', mover_producto, name="mover_producto"),
    path('search/', search_producto, name="search_producto"),
    path('darBaja/<int:id>', delete_producto, name="delete_producto"),
    path('moverGeneral/<int:id>/', mover_producto_detalle_general, name="mover_producto_detalle_general"),
    path('list_ajuste_inventario_ajax/', list_ajuste_inventario_ajax, name="list_ajuste_inventario_ajax"),
    path('list_ajustar_inventario/', list_ajustar_inventario, name="list_ajustar_inventario"),
    path('addAjusteInventario/', add_ajuste_inventario, name="add_ajuste_inventario"),
    path('list_ajuste_inventario_historial_ajax/', list_ajuste_inventario_historial_ajax, name="list_ajuste_inventario_historial_ajax"),
    path('list_ajustar_historial_inventario/', list_ajustar_historial_inventario, name="list_ajustar_historial_inventario"),
    path('get_producto_inventario/', get_producto_inventario, name="get_producto_inventario"),
    path('get_producto_antiparasitario/', get_producto_antiparasitario, name="get_producto_antiparasitario"),
    path('listHistoricoCompra/<int:id>/', list_historico_producto, name="list_historico_producto"),
    path('get_historico_producto/<int:id>/', get_historico_producto, name="get_historico_producto"),
   
]