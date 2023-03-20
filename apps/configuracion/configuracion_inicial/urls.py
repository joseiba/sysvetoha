from django.urls import path
from .views import *

urlpatterns = [
    #Urls Configuraciones
    path('listHistorialTimbrado/', list_historial_timbrado , name="list_historial_timbrado"),
    path('get_historial_timbrado_ajax/', get_historial_timbrado_ajax , name="get_historial_timbrado_ajax"),
    path('confiInicial/', confi_inicial, name="confi_inicial"),
]