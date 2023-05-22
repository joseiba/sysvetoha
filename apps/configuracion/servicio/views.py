from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import math

from apps.configuracion.servicio.forms import ServicioForm
from apps.configuracion.servicio.models import Servicio
from apps.inventario.productos.models import Producto


# Create your views here.
#Servicios
@login_required()
@permission_required('servicio.add_servicio')
def add_servicio(request):
    form = ServicioForm    
    if request.method == 'POST':
        form = ServicioForm(request.POST) 
        if form.is_valid():           
            ser = form.save(commit=False)
            ser.save()
            pro = Producto()
            pro.codigo_producto = request.POST.get("cod_serv")
            pro.nombre_producto = request.POST.get("nombre_servicio")
            pro.descripcion = request.POST.get("nombre_servicio")
            pro.precio_compra = request.POST.get("precio_servicio")
            pro.precio_venta = request.POST.get("precio_servicio")
            pro.stock_minimo = 0
            pro.stock = 1
            pro.stock_total = 1000
            pro.servicio_o_producto = 'S'
            pro.id_servicio = ser.id
            pro.save()        
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/configuracion/listServicio')
    context = {'form' : form}
    return render(request, 'configuracion/servicio/add_servicio_modal.html', context)

@login_required()
@permission_required('servicio.add_servicio')
def add_servicio_from_empleado(request):
    form = ServicioForm    
    if request.method == 'POST':
        form = ServicioForm(request.POST) 
        if form.is_valid():           
            ser = form.save(commit=False)
            ser.save()                    
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/configuracion/listEmpleado/')
    context = {'form' : form, 'from_add': 'S'}
    return render(request, 'configuracion/servicio/add_servicio_modal.html', context)

@login_required()
@permission_required('servicio.change_servicio')
def edit_servicio(request, id):
    servicios = Servicio.objects.get(id=id)
    form = ServicioForm(instance=servicios)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicios)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/configuracion/listServicio/')
        if form.is_valid():
            servicios = form.save(commit=False)
            servicios.save()
            pro = Producto.objects.get(id_servicio=id)
            pro.codigo_producto = request.POST.get("cod_serv")
            pro.nombre_producto = request.POST.get("nombre_servicio")
            pro.descripcion = request.POST.get("nombre_servicio")
            pro.precio_compra = request.POST.get("precio_servicio")
            pro.precio_venta = request.POST.get("precio_servicio")
            pro.id_servicio = servicios.id
            pro.save()           
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/configuracion/listServicio/')
    context = {'form' : form, 'servicios': servicios}
    return render(request, 'configuracion/servicio/edit_servicio_modal.html', context)

@login_required()
@permission_required('servicio.view_servicio')
def list_servicio(request):
    servicios = Servicio.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(servicios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "configuracion/servicio/list_servicio.html", context)

@login_required()
def list_servicio_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        servicios = Servicio.objects.exclude(is_active="N").filter(Q(nombre_servicio__icontains=query))
    else:
        servicios = Servicio.objects.exclude(is_active="N").order_by('-last_modified')

    total = servicios.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        clientes = clientes[start:start + length]

    data = [{'id': ser.id, 'nombre': ser.nombre_servicio, 'precio': ser.precio_servicio } for ser in servicios]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

#Metodo para eliminar servicio
@login_required()
@permission_required('servicio.delete_servicio')
def bajar_servicio(request, id):
    try:
        servicio = Servicio.objects.get(id=id)       
        servicio.is_active = "N"
        servicio.save()
        response = {
            "mensaje": "OK"
        }
        return JsonResponse(response)
    except Exception as e:        
        response = {'mensaje':"Error" }
        return JsonResponse(response)


@login_required()
def search_servicio(request):
    query = request.GET.get('q')
    if query:
        servicios = Servicio.objects.exclude(is_active="N").filter(Q(nombre_servicio__icontains=query))
    else:
        servicios = Servicio.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(servicios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "configuracion/servicio/list_servicio.html", context)

