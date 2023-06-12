import json
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods, require_safe
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import  Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

from apps.ventas.views import return_product
from apps.configuracion.configuracion_inicial.models import ConfiEmpresa
from apps.compras.models import Proveedor, Pedido, FacturaCompra, FacturaDet, PedidoCabecera, PedidoDetalle
from apps.compras.forms import ProveedorForm, PedidoForm, FacturaCompraForm
from apps.inventario.productos.models import Producto
from apps.caja.models import Caja


date = datetime.now()
today = date.strftime("%d/%m/%Y")
# Create your views here.
@require_http_methods(["POST","GET"])
@login_required()
@permission_required('compras.add_proveedor')
def add_proveedor(request):
    form = ProveedorForm    
    if request.method == 'POST':
        form = ProveedorForm(request.POST) 
        if form.is_valid():           
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')           
            return redirect('/compra/listProveedor')
    context = {'form' : form}
    return render(request, 'compras/proveedor/add_proveedor_modal.html', context)

@require_http_methods(["POST","GET"])
@login_required()
@permission_required('compras.change_proveedor')
def edit_proveedor(request, id):
    proveedor = Proveedor.objects.get(id=id)
    form = ProveedorForm(instance=proveedor)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/compra/listProveedor')
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.save()
            messages.success(request, 'Se ha editado correctamente!')         
            return redirect('/compra/listProveedor')
    context = {'form' : form, 'proveedor': proveedor}
    return render(request, 'compras/proveedor/edit_proveedor_modal.html', context)

@require_http_methods(["GET"])
@login_required()
@permission_required('compras.view_proveedor')
def list_proveedor(request):
    return render(request, "compras/proveedor/list_proveedor.html")

@require_http_methods(["GET"])
@login_required()
def list_proveedor_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        proveedor = Proveedor.objects.exclude(is_active="N").filter(Q(nombre_proveedor__icontains=query) | Q(ruc_proveedor__icontains=query))
    else:
        proveedor = Proveedor.objects.exclude(is_active="N").order_by('-last_modified')

    total = proveedor.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        proveedor = proveedor[start:start + length]

    data = [{'id': pro.id, 'nombre': pro.nombre_proveedor, 'direccion': pro.direccion, 
    'ruc': pro.ruc_proveedor, 'telefono' : pro.telefono, 'email': pro.email } for pro in proveedor]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

#Metodo para eliminar servicio
@require_http_methods(["GET","POST"])
@login_required()
@permission_required('compras.delete_proveedor')
def delete_proveedor(request, id):
    proveedor = Proveedor.objects.get(id=id)    
    if request.method == 'POST':          
        proveedor.is_active = "N"
        proveedor.save()
        return redirect('/compra/listProveedor')
    context = {"proveedor": proveedor}
    return render(request, 'compras/proveedor/baja_proveedor_modal.html', context)


def add_pedido():
    producto = Producto.objects.exclude(is_active='N').all()
    for pro in producto:
        pe = pro.id
        try:
            pedi = Pedido.objects.get(id_producto=pe)
            if pro.stock_minimo <= pro.stock:
                pedi.is_active = "N"
                pedi.save()
            if pro.stock_minimo >= pro.stock:
                pedi.is_active = "S"
                pedi.save()                
        except:
            if pro.stock_minimo >= pro.stock:
                pedido = Pedido()
                pedido.id_producto = pro
                pedido.cantidad_pedido = '-'
                pedido.save()            

@require_http_methods(["GET"])
@login_required()
def list_pedido(request):
    add_pedido()
    return render(request, "compras/pedidos/list_pedidos.html")

@require_http_methods(["GET"])
@login_required()
def list_pedido_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        pedido = Pedido.objects.filter(Q(id_producto__nombre_producto__icontains=query)).order_by('-last_modified')
    else:
        pedido = Pedido.objects.order_by('-last_modified')

    total = pedido.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        pedido = pedido[start:start + length]

    data = [{'id': pe.id, 'nombre': pe.id_producto.nombre_producto, 'precio': pe.id_producto.precio_compra, 
    'cantidad': pe.cantidad_pedido, 'stock': pe.id_producto.stock, 'fecha_pedido': pe.fecha_alta, 'pedido_cargado': pe.pedido_cargado} for pe in pedido]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@require_http_methods(["GET"])
@login_required()
def edit_pedido(request, id):
    pedido = Pedido.objects.get(id=id)
    form = PedidoForm(instance=pedido)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/compra/listPedido')
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/compra/listPedido')
    context = {'form' : form, 'pedido': pedido}
    return render(request, 'compras/pedidos/edit_pedido_modal.html', context)


#Facturas compras
@login_required()
@permission_required('compras.add_facturacompra')
def add_factura_compra(request):
    form = FacturaCompraForm()
    mensaje = ""
    if request.method == 'POST' and is_ajax(request=request):
        try:        
            factura_dict = json.loads(request.POST['factura'])
            try:
                factura = FacturaCompra()
                factura.nro_factura = factura_dict['nro_factura']
                factura.nro_timbrado = factura_dict['nro_timbrado']
                proveedor_id = Proveedor.objects.get(id=factura_dict['proveedor'])           
                factura.id_proveedor = proveedor_id
                factura.fecha_emision = factura_dict['fecha_emision']
                factura.fecha_vencimiento = factura_dict['fecha_vencimiento']
                factura.estado = 'PENDIENTE'
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])                
                factura.save()
                factura_id = FacturaCompra.objects.get(id=factura.id)
                for i in factura_dict['products']:
                    detalle = FacturaDet()
                    detalle.id_factura = factura_id                    
                    pedido_id = Pedido.objects.get(id=i['codigo_producto'])
                    pedido_id.pedido_cargado = "S"
                    pedido_id.save()            
                    detalle.id_pedido =pedido_id
                    detalle.cantidad = int(i['cantidad'])
                    detalle.descripcion = i['description']
                    detalle.save()
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
    context = {'form': form, 'calc_iva': 5, 'accion': 'A'}
    return render(request, 'compras/factura/add_factura_compra.html', context)

#Refactor de pedidos
@require_http_methods(["GET"])
@login_required()
@permission_required('compras.view_pedidocabecera')
def list_pedido_compra(request):
    add_pedido()
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() > 0:
        abierto = "S"
    else:
        abierto = "N"
    context = {'caja_abierta' : abierto}
    return render(request, 'compras/pedidos/list_pedidos_compras.html', context)

@require_http_methods(["GET"])
def list_pedido_compra_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        pedidoCabecera = PedidoCabecera.objects.exclude(is_active="N").filter(Q(id__icontains=query)).order_by('-last_modified')
    else:
        pedidoCabecera = PedidoCabecera.objects.exclude(is_active="N").order_by('-last_modified')

    total = pedidoCabecera.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)

        pedidoCabecera = pedidoCabecera[start:start + length]

    data = [{'id': pc.id, 'fecha_pedido': pc.fecha_alta, 'pedido_cargado':pc.pedido_cargado} for pc in pedidoCabecera]

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@require_http_methods(["GET","POST"])
@login_required()
@permission_required('compras.add_pedidocabecera')
def add_pedido_compra(request):
    pedidos = Pedido.objects.exclude(pedido_cargado='S').all()
    mensaje = ""
    if request.method == 'POST' and is_ajax(request=request):    
        try:        
            pedido_dict = json.loads(request.POST['pedido'])
            try:
                pedidoCabecera = PedidoCabecera()
                pedidoCabecera.save()
                pedido_cabecera_id = PedidoCabecera.objects.get(id=pedidoCabecera.id)
                for i in pedido_dict['products']:
                    pedido_detalle = PedidoDetalle()
                    pedido_detalle.id_pedido_cabecera = pedido_cabecera_id
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    pedido_detalle.id_producto = producto_id
                    pedido_detalle.cantidad = int(i['cantidad'])
                    pedido_detalle.descripcion = i['description']
                    pedido_detalle.save()
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
    context = {'accion': 'A', 'pedidos': json.dumps(get_pedido_list()), 'pedidos_list': pedidos}
    return render(request, 'compras/pedidos/add_compra_pedido.html', context)

@require_http_methods(["GET","POST"])
@login_required()
@permission_required('compras.change_pedidocabecera')
def edit_pedido_compra(request, id):
    data = {}
    mensaje = ""
    if request.method == 'POST' and is_ajax(request=request):
        try:        
            pedido_dict = json.loads(request.POST['pedido'])
            try:
                pedidoCabecera = PedidoCabecera.objects.get(id=id)  
                pedido_detail = PedidoDetalle.objects.filter(id_pedido_cabecera=id)          
                pedido_detail.delete()
                for i in pedido_dict['products']:
                    pedido_detalle = PedidoDetalle()
                    pedido_detalle.id_pedido_cabecera = pedidoCabecera                   
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    pedido_detalle.id_producto = producto_id
                    pedido_detalle.cantidad = int(i['cantidad'])
                    pedido_detalle.descripcion = i['description']
                    pedido_detalle.save()
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
    context = {'det': json.dumps(get_detalle_pedido_compra(id)), 'accion': 'E', 'pedidos': json.dumps(get_pedido_list())}
    return render(request, 'compras/pedidos/edit_pedido_compra.html', context)   
    
def get_pedido_list():
    data = []
    produc = Producto.objects.exclude(is_active="N").all()

    for i in produc:
        item = i.obtener_dict()
        item['id'] = i.id
        producto_desc = '%s %s' % ('Producto: ' + i.nombre_producto, 
                                'Descripción: ' + i.descripcion)
        item['text'] = producto_desc

        data.append(item) 
    return data       


def get_detalle_pedido_compra(id):
    data = []
    try:
        detalles = PedidoDetalle.objects.filter(id_pedido_cabecera=id)
        for i in detalles:
            item = i.id_producto.obtener_dict()
            item['description'] = i.descripcion
            item['cantidad'] = i.cantidad
            data.append(item)
    except:
        pass
    return data


#Facturas compras
@require_http_methods(["GET","POST"])
@login_required()
@permission_required('compras.add_facturacompra')
def agregar_factura_compra(request):
    form = FacturaCompraForm()
    mensaje = ""
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() > 0:
        abierto = "S"
    else:
        abierto = "N"
    if request.method == 'POST' and is_ajax(request=request):
        try:        
            factura_dict = json.loads(request.POST['factura'])
            try:
                factura = FacturaCompra()
                factura.nro_factura = factura_dict['nro_factura']
                factura.nro_timbrado = factura_dict['nro_timbrado']
                proveedor_id = Proveedor.objects.get(id=factura_dict['proveedor'])           
                factura.id_proveedor = proveedor_id
                factura.fecha_emision = factura_dict['fecha_emision']
                factura.fecha_vencimiento = factura_dict['fecha_vencimiento']
                factura.factura_cargada_pedido = 'S'
                factura.facturado = 'S'
                factura.estado = 'PENDIENTE'
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])                
                factura.save()
                factura_id = FacturaCompra.objects.get(id=factura.id)
                for i in factura_dict['products']:
                    detalle = FacturaDet()
                    detalle.id_factura = factura_id    
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    producto_id.precio_compra = i['precio_compra']
                    producto_id.save()
                    detalle.precio_compra = i['precio_compra']
                    detalle.id_producto = producto_id
                    detalle.cantidad = int(i['cantidad'])
                    detalle.descripcion = i['description']
                    detalle.save()
                    producto_id.stock_total += int(i['cantidad'])
                    producto_id.stock += int(i['cantidad'])
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
    context = {'form': form, 'calc_iva': 5, 'accion': 'A', 'caja_abierta' : abierto}
    return render(request, 'compras/factura/add_factura_compra.html', context)



def add_factura_compra():
    pedido_cabecera = PedidoCabecera.objects.exclude(is_active='N').all()
    if pedido_cabecera is not None:
        for pediCabecera in pedido_cabecera:
            try: 
                if pediCabecera.pedido_cargado == 'N':
                    pediCabecera.pedido_cargado = 'S'
                    pediCabecera.save()
                    factura = FacturaCompra.objects.get(id_pedido_cabecera=pediCabecera.id)
                    factura_id = FacturaCompra.objects.get(id=factura.id)
                    if factura.factura_cargada_pedido == 'N':
                        factDetalle = FacturaDet.objects.filter(id_factura=factura.id)
                        factDetalle.delete()
                        pedido_detalle = PedidoDetalle.objects.filter(id_pedido_cabecera=pediCabecera.id)
                        for i in pedido_detalle:
                            detalle = FacturaDet()
                            detalle.id_factura = factura_id                  
                            producto_id = Producto.objects.get(id=i.id_producto.id)
                            detalle.id_producto = producto_id
                            detalle.cantidad = i.cantidad
                            detalle.descripcion = i.descripcion
                            detalle.save()                           
            except Exception as e:
                try:        
                    factura = FacturaCompra()
                    factura.id_pedido_cabecera = pediCabecera
                    factura.save()
                    factura_id = FacturaCompra.objects.get(id=factura.id)
                    pedido_detalle = PedidoDetalle.objects.filter(id_pedido_cabecera=pediCabecera.id)
                    for i in pedido_detalle:
                        detalle = FacturaDet()
                        detalle.id_factura = factura_id                  
                        producto_id = Producto.objects.get(id=i.id_producto.id)
                        detalle.id_producto = producto_id
                        detalle.cantidad = i.cantidad
                        detalle.descripcion = i.descripcion
                        detalle.save()                        
                except Exception as e:
                    pass

@require_http_methods(["GET","POST"])
@login_required()
@permission_required('compras.change_facturacompra')
def edit_factura_compra(request, id):
    factCompra = FacturaCompra.objects.get(id=id)
    form = FacturaCompraForm(instance=factCompra)
    mensaje = ""
    if request.method == 'POST' and is_ajax(request=request):
        try:        
            factura_dict = json.loads(request.POST['factura'])
            try:
                factura = FacturaCompra.objects.get(id=id)
                factura.nro_factura = factura_dict['nro_factura']
                factura.nro_timbrado = factura_dict['nro_timbrado']
                proveedor_id = Proveedor.objects.get(id=factura_dict['proveedor'])           
                factura.id_proveedor = proveedor_id
                factura.fecha_emision = factura_dict['fecha_emision']
                factura.fecha_vencimiento = factura_dict['fecha_vencimiento']
                factura.estado = 'PENDIENTE'
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])  
                factura.factura_cargada_pedido = 'S'
                factura.facturado = 'S'              
                factura.save()
                if (factura.id_pedido_cabecera):
                    pedido_cabecera = PedidoCabecera.objects.get(id=factura.id_pedido_cabecera)
                    pedido_cabecera.is_active = 'N'
                    pedido_cabecera.save()
                detailFact = FacturaDet.objects.filter(id_factura=id)
                detailFact.delete()
                for i in factura_dict['products']:
                    detalle = FacturaDet()
                    detalle.id_factura = factura
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    producto_id.precio_compra = i['precio_compra']
                    producto_id.save()
                    detalle.precio_compra = i['precio_compra']
                    detalle.id_producto = producto_id
                    detalle.cantidad = int(i['cantidad'])
                    detalle.descripcion = i['description']
                    detalle.save()
                    producto_id.stock_total += int(i['cantidad'])
                    producto_id.stock += int(i['cantidad'])
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
    context = {'form': form, 'det': json.dumps(get_detalle_factura(id)), 'accion': 'E', 'factuCompra': factCompra}
    return render(request, 'compras/factura/edit_factura_compra.html', context)

def get_detalle_factura(id):
    data = []
    try:
        detalles = FacturaDet.objects.filter(id_factura=id)
        for i in detalles:
            item = i.id_producto.obtener_dict()
            item['description'] = i.descripcion
            item['cantidad'] = i.cantidad
            item['precio_compra_viejo'] = i.precio_compra
            data.append(item)
    except:
        pass
    return data

@require_http_methods(["GET"])
@login_required()
@permission_required('compras.view_facturacompra')
def list_factura_compra(request):
    add_factura_compra()
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() > 0:
       abierto = "S"
    else:
        abierto = "N"
    context = {'caja_abierta' : abierto}
    return render(request, 'compras/factura/list_facturas.html', context)

@require_http_methods(["GET"])
def list_facturas_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        factCompra = FacturaCompra.objects.exclude(is_active="N").filter(Q(nro_factura__icontains=query) | Q(id_proveedor__ruc_proveedor__icontains=query) | Q(id_proveedor__nombre_proveedor__icontains=query)).order_by('last_modified')
    else:
        factCompra = FacturaCompra.objects.exclude(is_active="N").order_by('-last_modified')

    total = factCompra.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)      

        factCompra = factCompra[start:start + length]
    
    data= [{'id': fc.id,'nro_factura': fc.nro_factura, 'nro_timbrado': fc.nro_timbrado, 'fecha_emision': fc.fecha_emision, 'fecha_vencimiento': fc.fecha_vencimiento, 
            'proveedor': try_exception(fc.id_proveedor), 'im_total': fc.total} for fc in factCompra]     

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

def try_exception(id):
    try:
        pro = Proveedor.objects.get(id=id.id)
        return 'Nombre: ' + pro.nombre_proveedor + '</br> ' + 'Ruc: ' + pro.ruc_proveedor
    except Exception as e:
        return '-'

@require_http_methods(["GET", "POST"])
@login_required()
def search_pediddos_factura(request):
    data = {}
    try:
        term = request.POST['term']
        if (request.method == 'POST') and (request.POST['action'] == 'search_products'):
            data = []
            prods = Producto.objects.exclude(is_active='N').all()
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

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@require_http_methods(["GET"])
def reporte_compra_pdf(request, id):
    pedido_cabecera = PedidoCabecera.objects.get(id=id)
    confi = ConfiEmpresa.objects.get(id=1)
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    #self.cabecera(pdf)
    #Con show page hacemos un corte de página para pasar a la siguiente
    #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 18)
    #Dibujamos una cadena en la ubicación X,Y especificada
    pdf.drawString(210, 790, u"Orden de Compra")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, 760, u"Nombre: " + confi.nombre_empresa)
    pdf.drawString(30, 740, u"Direccion: " + confi.direccion)
    pdf.drawString(30, 720, u"Cuidad: " + confi.cuidad)
    pdf.drawString(300, 760, u"Fecha Pedido: " + pedido_cabecera.fecha_alta)
    pdf.drawString(300, 740, u"Nº Pedido: " + str(pedido_cabecera.id))
    y = 700
    tabla_report(pdf, y, id)

    pdf.showPage()
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def tabla_report(pdf, y, id):
    #Creamos una tupla de encabezados para neustra tabla
    encabezados = ('Codigo', 'Producto', 'Descripción', 'Cantidad', 'Precio \n Unitario', 'Total')

    pedido_detalle = PedidoDetalle.objects.filter(id_pedido_cabecera=id).order_by('last_modified')

    count_detalle = 2
    #Creamos una lista de tuplas que van a contener a las personas
    detalles = [(pedi.id_producto.id, pedi.id_producto.nombre_producto, 
                pedi.id_producto.descripcion, pedi.cantidad, '', '') for pedi in pedido_detalle]

    detalles_extras = [('', '', '', '', '', '') for i in range(count_detalle)]

    detalle_orden =  Table([encabezados] + detalles + detalles_extras, colWidths=[2.5 * cm, 3 * cm, 7* cm, 2 * cm, 3 * cm, 3 * cm])
        #Aplicamos estilos a las celdas de la tabla
    detalle_orden.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black), 
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]
    ))

    position = int(((pedido_detalle.count() + count_detalle) * 50 ) / (2))
    pdf.setFont("Helvetica", 12)
    pdf.drawString(480, ((680 - position)) , u"Total: ",)
    #Establecemos el tamaño de la hoja que ocupará la tabla 
    detalle_orden.wrapOn(pdf, 800, 600)
    #Definimos la coordenada donde se dibujará la tabla
    detalle_orden.drawOn(pdf, 10, 700 - position)