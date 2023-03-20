"""vetoho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import statistics
from django.contrib import admin
from django.urls import path, include
from cgitb import handler
from django.conf.urls.static import static
from vetoho import settings

#urls error page
from apps.handler.views import handler_404, handler_500

from apps.usuario.views import (Login, home_user, list_usuarios, list_usuarios_ajax, add_usuario, edit_usuario, add_rol, 
get_group_list, change_password, edit_rol, delete_rol, baja_usuario, list_usuarios_baja_ajax, alta_usuario, 
list_usuarios_baja, logoutUser)
#cliente
from apps.cliente.views import (add_ciudad, edit_ciudad, list_ciudades, get_list_ciudades, add_cliente,
edit_cliente, list_client_ajax, list_clientes, inactivar_cliente)

from apps.configuracion.servicio.views import (add_servicio, edit_servicio, bajar_servicio, list_servicio, search_servicio,
list_servicio_ajax, add_servicio_from_empleado)

from apps.configuracion.empleado.views import (add_empleado, bajar_empleado, edit_empleado, get_list_empleados_ajax, 
list_empleado, search_empleado)


urlpatterns = [
    path('SuperAdminUserDev/', admin.site.urls),
    path('', home_user, name="index"),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', logoutUser, name="logout"),
    
    #Usuarios
    path('usuario/listUsuarios/', list_usuarios, name="list_usuarios"),
    path('usuario/list_usuarios_ajax/', list_usuarios_ajax, name="list_usuarios_ajax"),
    path('usuario/list_usuarios_baja_ajax/', list_usuarios_baja_ajax, name="list_usuarios_baja_ajax"),
    path('usuario/add/', add_usuario , name="add_usuario"),
    path('usuario/edit/<int:id>/', edit_usuario, name="edit_usuario"),
    path('usuario/darBajaUsuario/<int:id>/', baja_usuario, name="baja_usuario"),
    path('usuario/altaUsuarios/<int:id>/', alta_usuario, name="alta_usuario"),
    path('usuario/addRol/', add_rol , name="add_rol"),
    path('usuario/editRol/<int:id>/', edit_rol , name="edit_rol"),
    path('usuario/eliminarRol/<int:id>/', delete_rol , name="delete_rol"),
    path('usuario/get_group_list/', get_group_list , name="get_group_list"),
    path('usuario/editPassword/<int:id>/', change_password , name="change_password"),
    path('usuario/listUsuariosBaja/', list_usuarios_baja, name="list_usuarios_baja"),

    #cliente urls
    path('configuracion/listCiudades/', list_ciudades , name="list_ciudades"),
    path('configuracion/get_list_ciudades/', get_list_ciudades , name="get_list_ciudades"),
    path('configuracion/addCiudad/',  add_ciudad, name="add_ciudad"),
    path('configuracion/editCiudad/<int:id>/',edit_ciudad , name="edit_ciudad"),
    path('cliente/addCliente/',add_cliente , name="add_cliente"),
    path('cliente/listCliente/', list_clientes, name="list_cliente"),
    path('cliente/get_list_client/', list_client_ajax, name="list_client_ajax"),
    path('cliente/editCliente/<int:id>/', edit_cliente, name="edit_cliente"),
    path('cliente/bajaCliente/<int:id>/', inactivar_cliente, name="inactivar_cliente"),

    #Productos
    path('producto/', include(('apps.inventario.productos.urls','producto'), namespace='producto')),
    path('deposito/', include(('apps.inventario.depositos.urls','deposito'), namespace='deposito')),

    #Servicios
    path('configuracion/listServicio/', list_servicio , name="list_servicio"),
    path('configuracion/addServicio/',  add_servicio, name="add_servicio"),
    path('configuracion/editServicio/<int:id>/',edit_servicio , name="edit_servicio"),
    path('configuracion/searchServicio/', search_servicio, name="search_servicio"),
    path('configuracion/get_list_servicio_ajax/', list_servicio_ajax , name="list_servicio_ajax"),
    path('configuracion/bajaServicio/<int:id>/', bajar_servicio, name="delete_servicio"),
    path('configuracion/addServicioFromEmpleado/', add_servicio_from_empleado, name="add_servicio_from_empleado"),


    #Empleados
    path('configuracion/listEmpleado/', list_empleado , name="list_empleado"),
    path('configuracion/get_list_servicio_ajax/', list_servicio_ajax , name="list_servicio_ajax"),
    path('configuracion/addEmpleado/',  add_empleado, name="add_empleado"),
    path('configuracion/editEmpleado/<int:id>/',edit_empleado , name="edit_empleado"),
    path('configuracion/searchEmpleado/', search_empleado, name="search_empleado"),
    path('configuracion/bajaEmpleado/<int:id>/', bajar_empleado, name="bajar_empleado"),
    path('configuracion/get_list_empleados_ajax/', get_list_empleados_ajax, name="get_list_empleados_ajax"),

    #Mascotas
    path('mascota/', include(('apps.mascotas.urls','mascota'), namespace='mascota')),
    
    #Ventas
    path('ventas/', include(('apps.ventas.urls','ventas'), namespace='venta')),

    #Configuraciones
    path('configuracion/', include(('apps.configuracion.configuracion_inicial.urls','configuracion_inicial'), namespace='configuracion_inicial')),

    #Utiles
    path('utiles/', include(('apps.utiles.urls','configuracion_inicial'), namespace='utiles')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404=handler_404
handler500=handler_500