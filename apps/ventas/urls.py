from django.urls import path
from .views import *

urlpatterns = [
    #Urls Ventas
    path('listFacturasVentas/', list_factura_ventas, name="list_factura_ventas"),
    path('get_list_facturas_ventas/', list_facturas__ventas_ajax, name="list_facturas__ventas_ajax"),
    path('addFacturaVenta/', add_factura_venta , name="add_factura_venta"),
    path('get_producto_servicio_factura/', get_producto_servicio_factura, name="get_producto_servicio_factura"),
    path('editFacturaVenta/<int:id>/', edit_factura_venta, name="edit_factura_venta"),
    path('anularFacturaVenta/<int:id>/', anular_factura_venta, name="anular_factura_venta"),
    path('get_list_facturas_anulas_ventas/', list_facturas_anuladas_ventas_ajax, name="list_facturas_anuladas_ventas_ajax"),
    path('verDetalleFacturaAnulada/<int:id>/', ver_factura_anulada_venta, name="ver_factura_anulada_venta"),
    path('validate_producto_stock/', validate_producto_stock , name="validate_producto_stock"),
    path('listFacturasVentasAnuladas/', list_facturas_ventas_anuladas, name="list_facturas_ventas_anuladas"),
    #path('reporteFactura/<int:id>/', reporte_factura_venta_pdf, name="reporte_factura_venta_pdf"),

]