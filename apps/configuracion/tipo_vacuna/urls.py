from django.urls import path
from .views import *

urlpatterns = [
    path('listVacunas/', list_vacunas , name="list_vacunas"),
    path('get_list_vacunas_ajax/', get_list_vacunas_ajax , name="get_list_vacunas_ajax"),
    path('addVacuna/',  add_vacuna, name="add_vacuna"),
    path('editVacuna/<int:id>/', edit_vacuna , name="edit_vacuna"),
    path('get_periodo_vacunacion/', get_periodo_vacunacion , name="get_periodo_vacunacion"),
]