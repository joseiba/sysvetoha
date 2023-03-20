from django.urls import path
from .views import *

urlpatterns = [
    #Urls Utiles
    # path('utiles/poner_vencido_timbrado/', poner_vencido_timbrado, name="poner_vencido_timbrado"),
    path('validate_nro_timbrado/', validate_nro_timbrado, name="validate_nro_timbrado"),
    path('validar_ruc/', validar_ruc, name="validar_ruc"),
]