from django.urls import path
from .views import (add_pedido_compra,add_proveedor,
                    agregar_factura_compra, list_factura_compra,list_facturas_ajax,list_pedido,list_pedido_ajax
                    ,list_pedido_compra,list_pedido_compra_ajax,list_proveedor,list_proveedor_ajax,edit_factura_compra,edit_pedido,
                    edit_pedido_compra,edit_proveedor,delete_proveedor, search_pediddos_factura,reporte_compra_pdf)

urlpatterns = [
    # Urls compras
    path('addProveedor/', add_proveedor, name="add_proveedor"),
    path('listProveedor/', list_proveedor, name="list_proveedor"),
    path('get_list_proveedor/', list_proveedor_ajax, name="list_proveedor_ajax"),
    path('editProveedor/<int:id>/', edit_proveedor, name="edit_proveedor"),
    path('deleteProveedor/<int:id>/', delete_proveedor, name="delete_proveedor"),
    # Pedidos

    path('listPedido/', list_pedido, name="list_pedido"),
    path('get_list_pedido/', list_pedido_ajax, name="list_pedido_ajax"),
    path('editPedido/<int:id>/', edit_pedido, name="edit_pedido"),
    path('listFacturasCompras/', list_factura_compra, name="list_factura_compra"),
    path('addFacturaCompra/', agregar_factura_compra, name="add_factura_compra"),
    path('editFacturaCompra/<int:id>/',
         edit_factura_compra, name="edit_factura_compra"),
    path('get_list_proveedor/', list_proveedor_ajax, name="list_proveedor_ajax"),
    path('get_list_facturas/', list_facturas_ajax, name="list_facturas_ajax"),
    path('get_pedido_factura/', search_pediddos_factura,
         name="search_pediddos_factura"),
    path('listPedidosCompra/', list_pedido_compra, name="list_pedido_compra"),
    path('list_pedido_compra_ajax/', list_pedido_compra_ajax,
         name="list_pedido_compra_ajax"),
    path('addPedidoCompra/', add_pedido_compra, name="add_pedido_compra"),
    path('editPedidoCompra/<int:id>/',
         edit_pedido_compra, name="edit_pedido_compra"),
    path('reporteCompra/<int:id>/', reporte_compra_pdf, name="reporte_compra_pdf"),
]
