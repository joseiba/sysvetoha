import json
import math
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime
#from io import BytesIO
#from reportlab.pdfgen import canvas
from django.views.generic import View
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
#from reportlab.lib.units import cm
#from reportlab.lib import colors
from django.core import serializers

from apps.ventas.models import CabeceraVenta, DetalleVenta
from apps.ventas.forms import DetalleVentaForm, CabeceraVentaForm
from apps.configuracion.servicio.models import Servicio
from apps.configuracion.configuracion_inicial.models import ConfiEmpresa
from apps.inventario.productos.models import Producto
from apps.cliente.models import Cliente
from apps.utiles.views import reset_nro_timbrado
from apps.caja.models import Caja

date = datetime.now()
today = date.strftime("%d/%m/%Y")
# Create your views here.

@login_required()
@permission_required('venta.view_cabeceraventa')
def list_factura_ventas(request):
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() > 0:
        abierto = "S"
    else:
        abierto = "N"
    context = {'caja_abierta' : abierto}
    return render(request, 'ventas/list_facturas_ventas.html', context)

def list_facturas__ventas_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        factVenta = CabeceraVenta.objects.exclude(is_active="N").filter(Q(nro_factura__icontains=query) | Q(nro_timbrado__icontains=query) | Q(id_cliente__nombre_cliente__icontains=query) 
            | Q(id_cliente__cedula__icontains=query) | Q(id_cliente__ruc__icontains=query)).order_by('-last_modified')
    else:
        factVenta = CabeceraVenta.objects.exclude(is_active="N").order_by('-last_modified')

    total = factVenta.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)      
        factVenta = factVenta[start:start + length]
    
    data= [{'id': fv.id,'nro_factura': fv.nro_factura, 'nro_timbrado': fv.nro_timbrado, 'fecha_emision': fv.fecha_emision, 
            'cliente': try_exception_cliente(fv.id_cliente), 'im_total': fv.total}for fv in factVenta]     

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@permission_required('venta.view_cabeceraventa')
def list_facturas_ventas_anuladas(request):    
    return render(request, 'ventas/list_facturas_anuladas.html')


def list_facturas_anuladas_ventas_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        factVenta = CabeceraVenta.objects.exclude(is_active="S").filter(Q(nro_factura__icontains=query) | Q(nro_timbrado__icontains=query) | Q(id_cliente__nombre_cliente__icontains=query) 
            | Q(id_cliente__cedula__icontains=query) | Q(id_cliente__ruc__icontains=query)).order_by('-last_modified')
    else:
        factVenta = CabeceraVenta.objects.exclude(is_active="S").order_by('-last_modified')

    total = factVenta.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)

        factVenta = factVenta[start:start + length]
    
    data= [{'id': fv.id,'nro_factura': fv.nro_factura, 'nro_timbrado': fv.nro_timbrado, 'fecha_emision': fv.fecha_emision, 
            'cliente': try_exception_cliente(fv.id_cliente), 'im_total': fv.total}for fv in factVenta]     

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

def try_exception_cliente(id):
    try:
        cli = Cliente.objects.get(id=id.id)
        if cli.ruc is None:
            ruc_cedula = cli.cedula
        else:
            ruc_cedula = cli.ruc
        return 'Nombre: ' + cli.nombre_cliente + " " + cli.apellido_cliente  +'</br> ' + 'Ruc/Cédula: ' + ruc_cedula
    except Exception as e:
        return '-'

@login_required()
@permission_required('venta.add_cabeceraventa')
def add_factura_venta(request):
    form = CabeceraVentaForm()
    confi = get_confi()
    mensaje = ""
    confi_initial = ConfiEmpresa.objects.get(id=1)
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() > 0:
        abierto = "S"
    else:
        abierto = "N" 
    if request.method == 'POST':
        try:
            confi = ConfiEmpresa.objects.get(id=1) 
            factura_dict = json.loads(request.POST['factura'])
            caja = Caja.objects.filter(apertura_cierre="A").first()
            try:
                factura = CabeceraVenta()
                factura.nro_factura = factura_dict['nro_factura']
                factura.nro_timbrado = confi.nro_timbrado
                factura.ruc_empresa = confi.ruc_empresa
                factura.contado_pos = factura_dict['contado_pos']
                factura.fecha_inicio_timbrado = confi.fecha_inicio_timbrado
                factura.fecha_fin_timbrado = confi.fecha_fin_timbrado
                cliente = Cliente.objects.get(id=factura_dict['cliente'])
                factura.id_cliente_id = cliente.id
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])
                factura.total_formateado = factura_dict['total_formated']
                factura.id_caja_id = caja.id
                factura.save()
                for i in factura_dict['products']:
                    detalle = DetalleVenta()
                    detalle.id_factura_venta_id = factura.id
                    producto = Producto.objects.get(id=i['codigo_producto'])
                    detalle.id_producto_id = producto.id
                    detalle.tipo = i['tipo']
                    detalle.cantidad = int(i['cantidad'])
                    detalle.descripcion = i['description']
                    detalle.subtotal = "Gs. " + "{:,}".format(int(i['subtotal'])).replace(",",".")
                    detalle.save()
                    producto.stock_total -= int(i['cantidad'])
                    producto.stock -= int(i['cantidad'])
                    producto.save()
                
                configuracion = ConfiEmpresa.objects.get(id=1)
                configuracion.nro_factura += 1
                configuracion.save()
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
    nro_factura_initial = reset_nro_timbrado(confi_initial.nro_timbrado)
    nro_factura = obtener_factura_formateada()
    context = {'form': form,  'calc_iva': 5, 'accion': 'A', 'confi': confi, 
               'nro_factura': nro_factura, 'productos': json.dumps(return_product()), 'caja_abierta': abierto}
    return render(request, 'ventas/add_factura_ventas.html', context)

def obtener_factura_formateada():
    try:
        configuracion = ConfiEmpresa.objects.get(id=1)
        numero = str(configuracion.nro_factura)
        cantidad_digito = 7 - len(numero)
        prefijo = '0' * cantidad_digito
        result = '00'+str(configuracion.nro_sucursal)+'-00'+str(configuracion.nro_caja)+'-'+prefijo+''+str(configuracion.nro_factura)
        return result
    except Exception as e:
        mensaje = 'Error'


@login_required()
@permission_required('venta.change_cabeceraventa')
def edit_factura_venta(request, id):
    factVenta = CabeceraVenta.objects.get(id=id)
    form = CabeceraVentaForm(instance=factVenta)
    confi = get_confi()
    data = {}
    mensaje = ""
    confi_initial = ConfiEmpresa.objects.get(id=1)
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() > 0:
        abierto = "S"
    else:
        abierto = "N" 
    if request.method == 'POST':
        try:        
            factura_dict = json.loads(request.POST['factura'])
            try:
                factura = CabeceraVenta.objects.get(id=id)
                factura.nro_factura = factura_dict['nro_factura']
                cliente_id = Cliente.objects.get(id=factura_dict['cliente'])
                factura.id_cliente = cliente_id
                factura.estado = 'PENDIENTE'
                factura.nro_timbrado = confi.nro_timbrado
                factura.ruc_empresa = confi.ruc_empresa
                factura.fecha_inicio_timbrado = confi.fecha_inicio_timbrado
                factura.fecha_fin_timbrado = confi.fecha_fin_timbrado
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])   
                factura.total_formateado = factura_dict['total_formated']             
                factura.save()
                detailFact = DetalleVenta.objects.filter(id_factura_venta=id)
                detailFact.delete()
                for i in factura_dict['products']:
                    detalle = DetalleVenta()
                    detalle.id_factura_venta = factura
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    detalle.id_producto = producto_id
                    detalle.tipo = i['tipo']
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
    context = {'form': form, 'det': json.dumps(get_detalle_factura(id)), 'accion': 'E', 'confi': confi, 'venta':factVenta,
               'productos': json.dumps(return_product()), 'caja_abierta': abierto}
    return render(request, 'ventas/edit_factura_venta.html', context)


@login_required()
@permission_required('venta.view_cabeceraventa')
def ver_factura_anulada_venta(request, id):
    factVenta = CabeceraVenta.objects.get(id=id)
    form = CabeceraVentaForm(instance=factVenta)
    confi = get_confi()
    context = {'form': form, 'det': json.dumps(get_detalle_factura(id)), 'accion': 'ANU', 'confi': confi, 'factVenta': factVenta}
    return render(request, 'ventas/ver_factura_anulada_venta.html', context)

@login_required()
@permission_required('venta.delete_cabeceraventa')
def anular_factura_venta(request, id):
    try:
        factVenta = CabeceraVenta.objects.get(id=id)
        factVenta.is_active = "N"
        factVenta.factura_caja = "S"
        factVenta.save()
        data = {
            'error':False, 
            'message':"Factura Anulada correctamente."
        }
    except CabeceraVenta.DoesNotExist:
        data = {
            'error':True, 
            'message':"No se encontro el registro."
        }
    return JsonResponse(data, safe=False)


def get_detalle_factura(id):
    data = []
    try:
        detalles = DetalleVenta.objects.filter(id_factura_venta=id)
        for i in detalles:
            item = i.id_producto.obtener_dict()
            item['description'] = i.descripcion
            item['cantidad'] = i.cantidad
            data.append(item)

    except Exception as e:
        pass
    return data

@login_required()
def get_producto_servicio_factura(request):
    data = {}
    try:
        term = request.POST['term']
        if (request.method == 'POST') and (request.POST['action'] == 'search_products'):
            data = []
            prods = Producto.objects.exclude(is_active='N').filter(nombre_producto__icontains=term)[0:10]
            for p in prods:
                item = p.obtener_dict()
                item['id'] = p.id
                producto_desc = '%s %s' % ('Producto: ' + p.nombre_producto, 
                                        'Descripción: ' + p.descripcion)
                item['text'] = producto_desc
                data.append(item)    
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


def get_confi():
    try:
        confi_empresa = ConfiEmpresa.objects.get(id=1)
        return confi_empresa
    except Exception as e:
        pass
        return ""


def validate_producto_stock(request):
    data = []
    mensaje = ""
    if request.method == 'POST':
        try:
            factura_dict = json.loads(request.POST['factura'])
            for i in factura_dict['products']:
                producto_id = Producto.objects.get(id=i['codigo_producto'])
                if producto_id.stock < int(i['cantidad']):
                    data.append(producto_id.nombre_producto)
            if len(data) > 0:
                mensaje = "F"
                response = {'mensaje':mensaje, 'data': json.dumps(data)}
                return JsonResponse(response)
            else:
                mensaje = "OK"
                response = {'mensaje':mensaje}
                return JsonResponse(response)
        except Exception as e:
            mensaje = 'error'
            response = {'mensaje':mensaje }
            return JsonResponse(response)
        
def return_product():
    data = []
    prods = Producto.objects.exclude(is_active='N').all()
    for p in prods:
        item = p.obtener_dict()
        item['id'] = p.id
        producto_desc = '%s %s' % ('Producto: ' + p.nombre_producto, 
                                'Descripción: ' + p.descripcion)
        item['text'] = producto_desc
        data.append(item)
    return data 