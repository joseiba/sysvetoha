from django.urls import path
from .views import *

urlpatterns = [
    #Urls deposito
    path('add/',add_deposito , name="add_deposito"),
    path('list/', list_deposito, name="list_deposito"),
    path('get_list_deposito/', get_list_deposito, name="get_list_deposito"),
    path('edit/<int:id>/', edit_deposito, name="edit_deposito"),
]