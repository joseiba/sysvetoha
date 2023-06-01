import math
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

from apps.caja.models import Caja
from apps.configuracion.configuracion_inicial.models import ConfiEmpresa
#from apps.compras.models import FacturaCompra
from apps.ventas.models import CabeceraVenta
from apps.compras.models import PedidoDetalle

# Create your views here.
date = datetime.now()
today = date.strftime("%d/%m/%Y")

@login_required()
@permission_required('caja.view_caja')
def list_cajas(request):
    return render(request, 'caja/apertura_caja.html')

@login_required()
def list_caja_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        caja = Caja.objects.exclude(apertura_cierre="C").filter(Q(fecha_hora_alta__icontains=query))
    else:
        caja = Caja.objects.exclude(apertura_cierre="C").all()

    total = caja.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        caja = caja[start:start + length]

    data = [{'id': ca.id, 'fecha_alta': ca.fecha_hora_alta, 'fecha_cierre': ca.fecha_cierre, 'saldo_inicial': ca.saldo_inicial, 
    'total_ingreso': ca.total_ingreso, 'total_egreso' : ca.total_egreso, 'saldo_entregar': ca.saldo_a_entregar, 'estado': ca.apertura_cierre } for ca in caja]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@permission_required('caja.view_caja')
def list_historico_caja(request):
    return render(request, 'caja/list_historial_caja.html')

@login_required()
def get_list_caja_historico(request):
    query = request.GET.get('busqueda')
    if query != "":
        caja = Caja.objects.exclude(apertura_cierre="A").filter(Q(fecha_hora_alta__icontains=query))
    else:
        caja = Caja.objects.exclude(apertura_cierre="A").all()

    total = caja.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)

        caja = caja[start:start + length]

    data = [{'id': ca.id, 'fecha_alta': ca.fecha_hora_alta, 'fecha_cierre': ca.fecha_cierre, 'saldo_inicial': ca.saldo_inicial, 
    'total_ingreso': ca.total_ingreso, 'total_egreso' : ca.total_egreso, 'saldo_entregar': ca.saldo_a_entregar, 'estado': ca.apertura_cierre } for ca in caja]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)


@login_required()
@permission_required('caja.add_caja')
def add_caja(request):
    monto_initial = get_config()
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() > 0:
        messages.success(request, 'Ya tienes una caja abierta!')
        return redirect('/caja/listCajas/')
    else:
        caja_cerrada = Caja.objects.exclude(apertura_cierre="A").filter(fecha_alta=today)
        if caja_cerrada.count() > 0:
            messages.success(request, 'Ya has hecho una apertura de caja en el dia!')
            return redirect('/caja/listCajas/')
        else:
            apertura = Caja()
            apertura.saldo_inicial = monto_initial
            apertura.saldo_inicial_formateado = "Gs. " + "{:,}".format(int(monto_initial)).replace(",",".")
            apertura.save()
            messages.success(request, 'Apertura de caja correctamente!')
            return redirect('/caja/listCajas/')

def cerrar_caja(request, id):
    try:
        caja_cierre = Caja.objects.get(id=id)
        if caja_cierre.apertura_cierre != "C":
            sum_total_compras = sum_factura_compra()
            caja_cierre.total_efectivo = sum_efectivo_factura_venta()
            caja_cierre.total_efectivo_formateado = "Gs. " + "{:,}".format(int(caja_cierre.total_efectivo)).replace(",",".")
            caja_cierre.total_pos = sum_pos_factura_venta()
            caja_cierre.total_pos_formateado = "Gs. " + "{:,}".format(int(caja_cierre.total_pos)).replace(",",".")
            sum_total_venta = sum_factura_venta()
            saldo_entregrar = sum_total_venta - caja_cierre.saldo_inicial
            caja_cierre.total_ingreso = sum_total_venta
            caja_cierre.total_ingreso_formateado = "Gs. " + "{:,}".format(int(sum_total_venta)).replace(",",".")
            caja_cierre.total_egreso = sum_total_compras
            caja_cierre.total_egreso_formateado = "Gs. " + "{:,}".format(int(sum_total_compras)).replace(",",".")
            if saldo_entregrar > 0:
                caja_cierre.saldo_a_entregar = saldo_entregrar
                caja_cierre.saldo_a_entregar_formateado = "Gs. " + "{:,}".format(int(saldo_entregrar)).replace(",",".")
            else:
                caja_cierre.saldo_a_entregar = 0
                caja_cierre.saldo_a_entregar_formateado = "Gs. " + "{:,}".format(0).replace(",",".")
            caja_cierre.apertura_cierre = "C"
            caja_cierre.fecha_cierre = date.strftime("%d/%m/%Y %H:%M:%S hs")
            caja_cierre.save()
            messages.success(request, 'Cierre de caja correctamente!')
            return redirect('/caja/listCajas/')
        else:
            messages.success(request, 'Esta caja ya esta cerrada!')
            return redirect('/caja/listCajas/')
    except Exception as e:
        messages.success(request, 'Ha ocurrido un error!')
        return redirect('/caja/listCajas/')



def sum_factura_compra():
    return 0


def sum_efectivo_factura_venta():
    try:
        factura_sin_anular = CabeceraVenta.objects.exclude(is_active="N").filter(fecha_alta=today)
        factura = factura_sin_anular.exclude(factura_caja="S")        
        su_efectivo = 0
        for fac in factura:
            if fac.contado_pos == "C":
                su_efectivo += fac.total                
        return su_efectivo
    except Exception as e:
        return 0

def sum_pos_factura_venta():
    try:
        factura_sin_anular = CabeceraVenta.objects.exclude(is_active="N").filter(fecha_alta=today)
        factura = factura_sin_anular.exclude(factura_caja="S")
        su_pos = 0
        for fac in factura:
            if fac.contado_pos == "P":
                su_pos += fac.total                
        return su_pos
    except Exception as e:
        return 0


def sum_factura_venta():
    try:
        factura_sin_anular = CabeceraVenta.objects.exclude(is_active="N").filter(fecha_alta=today)
        factura = factura_sin_anular.exclude(factura_caja="S")        
        sum_total = 0
        for fac in factura:
            sum_total += fac.total
            fac.factura_caja = "S"
            fac.save()
        return sum_total
    except Exception as e:
        return 0


def get_config():
    try:
        confi = ConfiEmpresa.objects.get(id=1)
        monto_split = confi.apertura_caja_inicial.split('.')
        monto_formateado = ""
        for monto in monto_split:
            monto_formateado += monto
        return float(monto_formateado)
    except Exception as e:
        return 300000


def reporte_caja_pdf(request, id):
    caja = Caja.objects.get(id=id)
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
    pdf.drawString(210, 790, u"Detalle Caja del Dia")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, 760, u"Nombre Empresa: " + confi.nombre_empresa)
    pdf.drawString(30, 740, u"Direccion: " + confi.direccion)
    pdf.drawString(30, 720, u"Cuidad: " + confi.cuidad)
    pdf.drawString(300, 760, u"Fecha Apertura: " + caja.fecha_hora_alta)
    pdf.drawString(300, 740, u"Fecha Cierre: " + caja.fecha_cierre)
    y = 700

    pdf.drawString(50, 700, u"----------------------------------------------------Detalle--------------------------------------------------")

    pdf.drawString(50, 670, u"Saldo Inicial: ")
    pdf.drawString(200, 670, u"" + caja.saldo_inicial_formateado)

    pdf.drawString(50, 640, u"Total cobrado en Pos: ")
    pdf.drawString(200, 640, u"" + caja.total_pos_formateado)    

    pdf.drawString(50, 610, u"Total cobrado en Efectivo: ")
    pdf.drawString(200, 610, u"" + caja.total_efectivo_formateado)

    pdf.drawString(50, 580, u"Total a Ingreso del Dia: ")
    pdf.drawString(200, 580, u"" + caja.total_ingreso_formateado)

    pdf.drawString(50, 550, u"Saldo a entregar: ")
    pdf.drawString(200, 550, u"" + caja.saldo_a_entregar_formateado)

    #tabla_report(pdf, y, caja)

    pdf.showPage()
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def tabla_report(pdf, y, caja):
    #Creamos una tupla de encabezados para neustra tabla
    encabezados = ('Codigo', 'Producto', 'Descripción', 'Cantidad', 'Precio \n Unitario', 'Total')

    pedido_detalle = PedidoDetalle.objects.filter(id_pedido_cabecera=id).order_by('last_modified')

    count_detalle = 2
    #Creamos una lista de tuplas que van a contener a las personas
    detalles = [(pedi.id_pedido.id_producto.codigo_producto, pedi.id_pedido.id_producto.nombre_producto, 
                pedi.id_pedido.id_producto.descripcion, pedi.cantidad, '', '') for pedi in pedido_detalle]

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


