from django.urls import path
from .views import *

urlpatterns = [
    #Urls mascotas
    path('list/', list_mascotas , name="list_mascotas"),     
    path('add/',  add_mascota, name="add_mascota"),
    path('edit/<int:id>/',edit_mascota , name="edit_mascota"),
    path('searchMascota', search_mascota, name="search_mascota"),
    path('listEspecie/', list_especie , name="list_especie"),
    path('get_list_especie/', list_especie_ajax , name="list_especie_ajax"),
    path('addEspecie/',  add_especie, name="add_especie"),
    path('editEspecie/<int:id>/',  edit_especie, name="edit_especie"),
    path('searchEspecie/', search_especie, name="search_especie"),
    path('listRaza/', list_raza , name="list_raza"),
    path('get_list_raza/', get_list_raza_ajax , name="get_list_raza_ajax"),
    path('addRaza/',  add_raza, name="add_raza"),
    path('editRaza/<int:id>/',  edit_raza, name="edit_raza"),
    path('searchRaza/', search_raza, name="search_raza"),
    path('editFichaMedica/<int:id>/', edit_ficha_medica, name="edit_ficha_medica"),
    path('historial/<int:id>/', list_historial , name="list_historial"),
    path('get_prox_vacuna/', get_prox_vacuna, name="get_prox_vacuna"),
    path('get_list_historico_vacunas_aplicadas/', get_list_historico_vacunas_aplicadas, name="get_list_historico_vacunas_aplicadas"),
    path('get_list_historico_vacunas_proximas/', get_list_historico_vacunas_proximas, name="get_list_historico_vacunas_proximas"),
]