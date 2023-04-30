from django.urls import path
from .views import *

urlpatterns = [
     #Urls compras
    path('addProveedor/', add_proveedor , name="add_proveedor"),
    path('listProveedor/', list_proveedor, name="list_proveedor"),
    path('get_list_proveedor/', list_proveedor_ajax, name="list_proveedor_ajax"),
    path('editProveedor/<int:id>/', edit_proveedor, name="edit_proveedor"),
    path('deleteProveedor/<int:id>/', delete_proveedor, name="delete_proveedor"),
]