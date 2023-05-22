from django.urls import path
from .views import *

urlpatterns = [
    path('listCajas/', list_cajas, name="list_cajas"),
    path('get_list_caja/', list_caja_ajax, name="list_caja_ajax"),
    path('add/',add_caja , name="add_caja"),
    path('cerrar_caja/<int:id>/',cerrar_caja , name="cerrar_caja"),
    path('listHistoricoCajas/', list_historico_caja, name="list_historico_caja"),
    path('get_list_caja_historico/', get_list_caja_historico, name="get_list_caja_historico"),
    path('reporteCaja/<int:id>/', reporte_caja_pdf, name="reporte_caja_pdf")
]