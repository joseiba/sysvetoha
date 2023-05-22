from django.urls import path
from .views import *

urlpatterns = [
    #Urls Utiles
    path('validate_nro_timbrado/', validate_nro_timbrado, name="validate_nro_timbrado"),
    path('validar_ruc/', validar_ruc, name="validar_ruc"),
    path('get_reserva_today/', get_reserva_today , name="get_reserva_today"),
    path('get_vacunas_today/', get_vacunas_today , name="get_vacunas_today")
]