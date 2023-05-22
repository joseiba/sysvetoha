import math
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
import json
from django.http import JsonResponse

from apps.inventario.productos.forms import TipoProductoForm
from apps.inventario.productos.models import TipoProducto
from apps.inventario.depositos.models import Deposito
from apps.inventario.productos.forms import ProductoForm
from apps.inventario.productos.models import Producto, Inventario, HistoricoProductoPrecio, ProductoStock
from apps.configuracion.configuracion_inicial.models import ConfiEmpresa
from apps.ventas.models import CabeceraVenta, DetalleVenta

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
            return redirect('/producto/listGeneral/')
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
    try:
        confiEm = ConfiEmpresa.objects.get(id=1)
        depo = Deposito.objects.get(descripcion=confiEm.ubicacion_deposito_inicial)
        if request.method == 'POST':
            form = ProductoForm(request.POST or None)
            if form.is_valid():                            
                pro = form.save(commit=False)                
                pro.stock_total = request.POST.get('stock')
                pro.save()
                messages.add_message(request, messages.SUCCESS, 'Producto agregado correctamente!')
            return redirect('/producto/listGeneral/')
    except:
        messages.add_message(request, messages.SUCCESS, 'Se debe agregar primeramente un deposito en configuraciones iniciales!')
        context = {'form' : form}
        return redirect('/producto/listGeneral/')
    context = {'form' : form, 'deposito_inicial': depo.id}
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
            return redirect('/producto/listGeneral/')
        if form.is_valid():
            producto = form.save(commit=False)
            producto.stock_total = request.POST.get('stock')
            producto.save()
            messages.add_message(request, messages.SUCCESS, 'El producto se ha editado correctamente!')
            return redirect('/producto/listGeneral/')
    context = {'form': form, 'producto': producto, 'deposito_inicial': producto.id_deposito.pk}
    return render(request, 'inventario/productos/add_producto.html', context)    

@login_required()
@permission_required('productos.view_producto')
def list_productos_general(request):
    sum_anular_factura_venta_to_producto()
    return render(request, "inventario/productos/list_producto_general.html")


@login_required()
def list_producto_general_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        productos = Producto.objects.exclude(is_active="N").filter(Q(id__icontains=query) |Q(nombre_producto__icontains=query)).order_by('-last_modified')        
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")
    else:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")


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


def get_producto_antiparasitario(request):
    data = {}
    try:
        term = request.POST['term']
        if (request.POST['action'] == 'search_products'):
            data = []
            prods = Producto.objects.exclude(is_active='N').filter(nombre_producto__icontains=term)[0:10]
            for p in prods:
                item = p.obtener_dict()
                item['id'] = p.id
                producto_desc = '%s' % (p.nombre_producto)
                item['text'] = producto_desc
                data.append(item)    
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)

def poner_vencido_producto():
    produc = Producto.objects.exclude(is_active="N").all()
    produc = produc.exclude(producto_vencido="S").all()
    today = datetime.now()
    fechaDate = datetime(today.year, today.month, today.day)
    if produc is not None:
        try:
            for p in produc:
                if p.fecha_vencimiento is not None:
                    fecha_vencimiento_split = p.fecha_vencimiento.split('/')
                    fecha_vencimiento_compare = datetime(int(fecha_vencimiento_split[2]), int(fecha_vencimiento_split[1]), int(fecha_vencimiento_split[0]))
                    if fechaDate > fecha_vencimiento_compare:
                        p.producto_vencido = "S"
                        p.is_active = "N"
                        p.save()
        except Exception as e:
            pass


def sum_anular_factura_venta_to_producto():
    factVenta = CabeceraVenta.objects.exclude(is_active="S").all()
    if factVenta is not None:
        for fv in factVenta:
            if(fv.factura_anulada == 'N'):
                fv.factura_anulada = "S"
                fv.save()
                facDe = DetalleVenta.objects.filter(id_factura_venta=fv.id)
                for factDet in facDe:
                    try:
                        if factDet.tipo == 'P':
                            prod = Producto.objects.get(id=factDet.id_producto.id)
                            prod.stock = prod.stock + factDet.cantidad
                            prod.stock_total = prod.stock_total + factDet.cantidad                            
                            prod.save()
                    except Exception as e:
                        pass


@login_required()
@permission_required('producto.view_producto')
def list_producto(request,id):
    data = []
    data_detalle = []
    stock_movido_cero = 0
    try:
        product = Producto.objects.filter(id=id)

        data =[{'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_actual': p.stock, 
            'deposito': p.id_deposito.descripcion} for p in product]

        pro = Producto.objects.get(id=id)
        stock_movido_cero = pro.stock      
    except Exception as e:
        pass

    try:
        producto_detalle = ProductoStock.objects.filter(id_producto=id)
        data_detalle =[{'id': p.id, 'codigo': p.id_producto.id ,'nombre': p.id_producto.nombre_producto, 'descripcion': p.id_producto.descripcion, 
        'stock_movido': p.producto_stock, 'deposito': p.id_deposito.descripcion} for p in producto_detalle]
    except Exception as e:
        pass   

    context = {'producto_detalle': data, 'producto_movido': data_detalle, 'id_producto': id, 'stck_cero': stock_movido_cero}
    return render(request, "inventario/productos/list_producto.html", context)


@login_required()
@permission_required('producto.add_producto')
def mover_producto(request, id):
    producto_movido = Producto()
    producto_moved = ProductoStock()
    producto = Producto.objects.get(id=id)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        nombre_deposito = request.POST.get('id_deposito')
        cantidad = request.POST.get('stock')
        deposito = Deposito.objects.get(id=nombre_deposito)

        if producto.stock - int(cantidad) >= 0:
            producto.stock = producto.stock - int(cantidad)
        else:
            producto.stock = 0
        producto.save() 

        if int(cantidad) >= 0:
            producto_moved.producto_stock = int(cantidad)
        else:
            producto_moved.producto_stock = 0
        producto_moved.id_deposito = deposito
        producto_moved.id_producto = producto
        producto_moved.save()
        messages.add_message(request, messages.SUCCESS, 'El producto se ha movido correctamente!')

        return redirect('/producto/listDetalle/' + str(id))

    context = {'form': form, 'producto': producto}
    return render(request, 'inventario/productos/mover_producto.html', context)

@login_required()
def list_producto_general_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        productos = Producto.objects.exclude(is_active="N").filter(Q(id__icontains=query) |Q(nombre_producto__icontains=query)).order_by('-last_modified')        
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")
    else:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")


    total = productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        productos = productos[start:start + length]

    data =[{'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_total': p.stock_total} for p in productos]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

def list_producto_vencido_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        productos = Producto.objects.exclude(is_active="N").filter(
            Q(nombre_producto__icontains=query) | Q(id__icontains=query)).order_by('-last_modified')        
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="N")
    else:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="N")


    total = productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        productos = productos[start:start + length]

    data =[{'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_vencido': p.stock_total, 
    'fecha_vencimiento': p.fecha_vencimiento} for p in productos]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@permission_required('producto.delete_producto')
def delete_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.is_active = "N"
    producto.save()
    return redirect('/producto/listGeneral/')

@permission_required('producto.add_producto')
def mover_producto_detalle_general(request, id):
    try:
        pedido_trasladado = ProductoStock.objects.get(id=id)
        producto_general = Producto.objects.get(id=pedido_trasladado.id_producto.id)
        producto_general.stock = producto_general.stock + pedido_trasladado.producto_stock
        producto_general.stock_total = producto_general.stock
        producto_general.save()
        pedido_trasladado.delete()
        messages.add_message(request, messages.SUCCESS, 'El producto se ha movido correctamente a la lista general!')
        return redirect('/producto/listDetalle/' + str(pedido_trasladado.id_producto.id))
    except Exception as e:
        messages.add_message(request, messages.SUCCESS, 'ha ocurrido un error inesperado, intente más tarde!')        
        return redirect('/producto/listGeneral/')


@login_required()
def search_producto(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(Q(nombre_producto__icontains=query) | Q(codigo_producto__icontains=query) | Q(id_deposito__descripcion__icontains=query)).order_by('-last_modified')
    else:
        productos = Producto.objects.all().order_by('-last_modified')
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "inventario/productos/list_producto.html", context)

# Ajuste de Inventario
@login_required()
@permission_required('producto.view_inventario')
def list_ajustar_inventario(request):
    #add_factura_to_producto()
    #rest_factura_venta_to_producto()
    sum_anular_factura_venta_to_producto()
    poner_vencido_producto()
    return render(request, "inventario/productos/list_ajuste_inventario.html")


def list_ajuste_inventario_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        productos = Producto.objects.exclude(is_active="N").filter(Q(id__icontains=query) |Q(nombre_producto__icontains=query) |Q(tipo_producto__nombre_tipo__icontains=query)).order_by('-last_modified')        
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")
        productos = productos.exclude(stock_total=0)
    else:
        productos = Producto.objects.exclude(is_active= "N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")
        productos = productos.exclude(stock_total=0)


    total = productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        productos = productos[start:start + length]

    data =[{'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_total': p.stock_total,
            'stock_fisico': 0} for p in productos]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@permission_required('producto.add_inventario')
def add_ajuste_inventario(request):
    mensaje = ""
    if request.method == 'POST' and is_ajax(request=request):
        try:
            ajustes_dict = json.loads(request.POST['ajuste'])
            try:
                for i in ajustes_dict['products']:
                    inve = Inventario()
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    inve.id_producto = producto_id
                    inve.stock_fisico = int(i['cantidad'])
                    inve.stock_viejo = producto_id.stock_total
                    inve.diferencia = int(i['cantidad']) - producto_id.stock_total 
                    producto_id.stock_total = int(i['cantidad'])
                    producto_id.stock = int(i['cantidad'])
                    inve.save()
                    producto_id.save()
                response = {'mensaje':mensaje }
                return JsonResponse(response)
            except Exception as e:
                mensaje = 'error'
                response = {'mensaje':mensaje }
                return JsonResponse(response)
        except Exception as e:
            mensaje = 'error'
            response = {'mensaje':mensaje }
            return JsonResponse(response)
    return render(request, 'inventario/productos/add_ajuste_inventario.html')


@login_required()
def get_producto_inventario(request):
    data = {}
    try:
        term = request.POST['term']
        if (request.method == 'POST') and (request.POST['action'] == 'search_products'):
            data = []
            prods = Producto.objects.exclude(is_active='N').all()
            prods = prods.exclude(stock_total=0).all()
            prods = prods.exclude(servicio_o_producto="S").filter(nombre_producto__icontains=term)[0:10]
            for p in prods:
                item = p.obtener_dict()
                item['id'] = p.id
                producto_desc = '%s %s' % ('Producto: ' + p.nombre_producto ,
                                        'Descripción: ' + p.descripcion)
                item['text'] = producto_desc
                data.append(item)
    except Exception as e:
        data['error'] = str(e)

    return JsonResponse(data, safe=False)

#Historico Inventario
@login_required()
@permission_required('producto.view_inventario')
def list_ajustar_historial_inventario(request):
    return render(request, "inventario/productos/list_historial_ajuste.html")


def list_ajuste_inventario_historial_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        inve = Inventario.objects.filter(Q(id_producto__id__icontains=query) | Q(id_producto__nombre_producto__icontains=query) | Q(id_producto__tipo_producto__nombre_tipo__icontains=query))
    else:
        inve = Inventario.objects.all()

    total = inve.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        inve = inve[start:start + length]

    data =[{'id': p.id_producto.id, 'nombre': p.id_producto.nombre_producto, 'descripcion': p.id_producto.descripcion, 'stock_total': p.stock_viejo,
            'stock_fisico': p.stock_fisico, 'diferencia': p.diferencia ,'fecha_ajuste': p.fecha_alta} for p in inve]        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)


#Historico Producto
@login_required()
@permission_required('producto.view_inventario')
def list_historico_producto(request, id):
    context = {'id_producto': id}
    return render(request, "inventario/productos/list_historial_producto_precio.html", context)


def get_historico_producto(request, id):
    query = request.GET.get('busqueda')
    if query != "":
        productos = HistoricoProductoPrecio.objects.filter(id_producto=id)
        productos = productos.filter(Q(id_producto__nombre_producto__icontains=query) | Q(fecha_alta__icontains=query))
    else:
        productos = HistoricoProductoPrecio.objects.filter(id_producto=id)


    total = productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        productos = productos[start:start + length]

    data =[{'nombre': p.id_producto.nombre_producto, 'descripcion': p.id_producto.descripcion, 
            'precio_compra': p.precio_compra, 'fecha_compra': p.fecha_alta} for p in productos]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
