import math
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import json
from django.http import JsonResponse

from apps.inventario.productos.forms import TipoProductoForm
from apps.inventario.productos.models import TipoProducto
from apps.inventario.depositos.models import Deposito
from apps.inventario.productos.forms import ProductoForm
from apps.inventario.productos.models import Producto

date = datetime.now()

#Metodo para agregar tipo producto
@login_required()
@permission_required('productos.add_tipoproducto')
def add_tipo_producto(request):
    form = TipoProductoForm
    if request.method == 'POST':
        form = TipoProductoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Tipo de producto agregado correctamente!')
            return redirect('/producto/tipoProducto/list')
    context = {'form' : form}
    return render(request, 'inventario/tipoProducto/add_tipo_producto.html', context)


# Metodo para editar tipo producto
@login_required()
@permission_required('productos.change_tipoproducto')
def edit_tipo_producto(request, id):
    tipo_producto = TipoProducto.objects.get(id=id)
    form = TipoProductoForm(instance=tipo_producto)
    if request.method == 'POST':
        form = TipoProductoForm(request.POST, instance=tipo_producto)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/producto/tipoProducto/list/')
        if form.is_valid():
            tipo_producto = form.save(commit=False)
            tipo_producto.save()
            messages.add_message(request, messages.SUCCESS, 'Tipo de producto editado correctamente!')
            return redirect('/producto/tipoProducto/list/')

    context = {'form': form, 'tipo_producto':tipo_producto}
    return render(request, 'inventario/tipoProducto/edit_tipo_producto.html', context)

# Metodo para dar de baja tipo producto
@login_required()
@permission_required('productos.delete_tipoproducto')
def baja_tipo_producto(request, id):
    try:
        tipo_producto = TipoProducto.objects.get(id=id)
        tipo_producto.is_active = "N"
        tipo_producto.save()
        response = {
            "mensaje": "OK"            
        }
        return JsonResponse(response)   
    except Exception as e:        
        response = {'mensaje':"Error" }
        return JsonResponse(response)


# Metodo para dar de alta tipo producto
@login_required()
@permission_required('productos.add_tipoproducto')
def alta_tipo_producto(request, id):
    tipo_producto = TipoProducto.objects.get(id=id)
    if request.method == 'POST':
        if tipo_producto.fecha_baja != "-":
            tipo_producto.is_active = "Y"
            tipo_producto.fecha_baja = '-'
            tipo_producto.save()
            return redirect('/producto/tipoProducto/list/')
        else:
            messages.success(request, 'El tipo de producto ya fue dado de alta!')
            return redirect('/producto/tipoProducto/list/')
    context = {'tipo_producto':tipo_producto}
    return render(request, 'inventario/tipoProducto/alta_tipo_producto.html', context)

    #Metodo para agregar tipo producto
@login_required()
@permission_required('productos.add_tipoproducto')
def add_tipo_producto_from_producto(request):
    form = TipoProductoForm
    if request.method == 'POST':
        form = TipoProductoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Tipo de producto agregado correctamente!')
            form = ProductoForm
            context = {'form' : form}
            return redirect('/producto/list/')
    context = {'form' : form, 'from_add': 'S'}
    return render(request, 'inventario/tipoProducto/add_tipo_producto.html', context)
    

#Metodo para listar todos los tipos de productos
@login_required()
@permission_required('productos.view_tipoproducto')
def list_tipo_producto(request):
    return render(request, "inventario/tipoProducto/list_tipo_producto.html")


def get_list_tipo_producto(request):
    query = request.GET.get('busqueda')

    if query:
        tipos_productos = TipoProducto.objects.exclude(is_active="N").filter(Q(nombre_tipo__icontains=query))
    else:
        tipos_productos = TipoProducto.objects.exclude(is_active="N").order_by('-last_modified')

    total = tipos_productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        tipos_productos = tipos_productos[start:start + length]

    data = [{'id': tp.id, 'nombre_tipo': tp.nombre_tipo, 'fecha_alta': tp.fecha_alta } for tp in tipos_productos]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response) 

#Metodo para la busqueda de tipo de producto
def vence_si_no(request):
    tipo_producto = request.GET.get('tipo')
    tipo_producto_vence = TipoProducto.objects.get(id=tipo_producto)

    if tipo_producto_vence.vence == 'S':
        response = {
            'mensaje' : 'S'
        }

        return JsonResponse(response)
    
    response = {
        'mensaje' : 'N'
    }

    return JsonResponse(response)


#Metodo Productos
@login_required()
@permission_required('productos.add_producto')
def add_producto(request):
    form = ProductoForm
    print(request)
    if request.method == 'POST':
        form = ProductoForm(request.POST or None)
        print(form)
        if form.is_valid():  
            print(form)                          
            pro = form.save(commit=False)                
            #pro.stock_total = request.POST.get('stock')
            pro.save()
            messages.add_message(request, messages.SUCCESS, 'Producto agregado correctamente!')
            return redirect('/producto/list/')
    context = {'form' : form}
    return render(request, 'inventario/productos/add_producto.html', context)

# Metodo para editar Productos
@login_required()
@permission_required('productos.change_producto')
def edit_producto(request, id):
    producto = Producto.objects.get(id=id)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/producto/list/')
        if form.is_valid():
            producto = form.save(commit=False)
            #producto.stock_total = request.POST.get('stock')
            producto.save()
            messages.add_message(request, messages.SUCCESS, 'El producto se ha editado correctamente!')
            return redirect('/producto/list/')
    context = {'form': form, 'producto': producto}
    return render(request, 'inventario/productos/add_producto.html', context)    

@login_required()
@permission_required('productos.view_producto')
def list_productos_general(request):
    return render(request, "inventario/productos/list_producto.html")


@login_required()
def list_producto_general_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        productos = Producto.objects.exclude(is_active="N").filter(Q(id__icontains=query) |Q(nombre_producto__icontains=query)).order_by('-last_modified')        
        #productos = productos.exclude(servicio_o_producto="S")
        #productos = productos.exclude(producto_vencido="S")
    else:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        #productos = productos.exclude(servicio_o_producto="S")
        #productos = productos.exclude(producto_vencido="S")


    total = productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        productos = productos[start:start + length]

    data =[{'codigo': p.id, 'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_total': p.stock} for p in productos]        
    print(data)
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)
