from django.urls import path
from apps.reportes.views import (get_producto_minimo, reporte_stock_a_vencer, reporte_stock_minimo, get_producto_vencimiento,
                                 reporte_vacunas_aplicadas, get_producto_minimo, get_producto_minimo, reporte_get_vacunas_aplicada, 
                                 reporte_prod_vendido, reporte_producto, reporte_servicio_vendido, get_proximas_vacunas, 
                                 get_servicio_vendido, list_proximas_vacunas)

urlpatterns = [
    path('listReporteProductoVendidos/', reporte_producto, name="reporte_producto"),
    path('get_productos_vendidos/', reporte_prod_vendido, name="reporte_prod_vendido"),
    path('listProductosMinimos/', reporte_stock_minimo, name="reporte_stock_minimo"),
    path('get_producto_minimo/',get_producto_minimo, name="get_producto_minimo"),
    path('listProductosVencimiento/', reporte_stock_a_vencer, name="reporte_stock_a_vencer"),
    path('get_producto_vencimiento/',get_producto_vencimiento, name="get_producto_vencimiento"),
    path('listServiciosVendidos/', reporte_servicio_vendido, name="reporte_servicio_vendido"),
    path('get_servicio_vendido/',get_servicio_vendido, name="get_servicio_vendido"),
    path('listProximasVacunaciones/', list_proximas_vacunas, name="list_proximas_vacunas"),
    path('get_proximas_vacunas/',get_proximas_vacunas, name="get_proximas_vacunas"),
    path('listVacunasAplicadas/', reporte_vacunas_aplicadas, name="reporte_vacunas_aplicadas"),
    path('get_vacunas_aplicadas/', reporte_get_vacunas_aplicada, name="reporte_get_vacunas_aplicada")


]

    