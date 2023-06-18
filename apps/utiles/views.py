from django.http import JsonResponse
from datetime import date, datetime

from apps.utiles.models import Timbrado
from apps.ventas.models import CabeceraVenta, DetalleVenta
from apps.cliente.models import Cliente
from apps.compras.models import Proveedor
from apps.configuracion.configuracion_inicial.models import ConfiEmpresa
from apps.inventario.productos.models import Producto
from apps.mascotas.models import HistoricoFichaMedica
from apps.agendamientos.models import Reserva
from apps.mascotas.models import Mascota
from apps.usuario.models import User
from apps.utiles.models import VacunasAplicadas, ServicioVendido, ProductoVendido
from apps.utiles.models import ProductoVendidoMes

hoy = date.today()
# Create your views here.
label_mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto',
            'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
# Create your views here.
def reset_nro_timbrado(nro_timbrado):
    if nro_timbrado is not None:
        try:    
            factura = CabeceraVenta.objects.filter(nro_timbrado=nro_timbrado)
            if factura.count() > 0:
                nro_factura = factura.count() + 1
            else:
                nro_factura = 1
        except Exception as e:
            nro_factura = 1
    else:
        nro_factura = 1
    return nro_factura

def poner_vencido_timbrado(request):
    mensaje = ""
    try:
        timbrado = Timbrado.objects.get(nro_timbrado=request.GET.get('nro_timbrado'))
        timbrado.vencido = "S"
        timbrado.save()
        mensaje = "OK"
        response = {"mensaje": mensaje}
        return JsonResponse(response)
    except Exception as e:
        response = {"mensaje": "ERROR"}
        return JsonResponse(response)


def validate_nro_timbrado(request):
    mensaje = ""
    try:
        timbrado_vencido = Timbrado.objects.get(nro_timbrado=request.GET.get('nro_timbrado'))
        if timbrado_vencido.vencido == "S":
            mensaje = "OK"
        response = {"mensaje": mensaje}
        return JsonResponse(response)
    except Exception as e:
        response = {"mensaje": mensaje}
        return JsonResponse(response)



def validar_ruc(request):
    obj_validar = request.GET.get('ruc')
    mensaje = ""
    try:
        if Cliente.objects.filter(ruc=obj_validar).exists():
            mensaje = 'EX'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
        elif Proveedor.objects.filter(ruc_proveedor=obj_validar).exists():
            mensaje = 'EX'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
        elif ConfiEmpresa.objects.filter(ruc_empresa=obj_validar):
            mensaje = 'EX'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
        else:
            mensaje = 'OK'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
    except Exception as e:
        mensaje = 'ER'
        response = {'mensaje': mensaje}
        return JsonResponse(response)
    

def total_user():
    try:
        usuario = User.objects.exclude(is_active=False).all()
        usuario = usuario.exclude(is_superuser=True)
        return usuario.count()
    except Exception as e:
        return 0

def total_cliente():
    try:
        cliente = Cliente.objects.exclude(is_active="N").all()
        return cliente.count()
    except Exception as e:
        return 0

def total_mascotas():
    try:
        mascotas = Mascota.objects.all()
        return mascotas.count()
    except Exception as e:
        return 0

def total_producto():
    try:
        productos = Producto.objects.exclude(is_active="N").all()        
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")
        return productos.count()
    except Exception as e:
        return 0

def total_stock_minimo():
    prod_minimo = []
    try:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")

        for p in productos:
            if p.stock_minimo >= p.stock_total:
                prod_minimo.append(p)

        total =  len(prod_minimo)
        return total
    except Exception as e:
        return 0

def total_productos_a_vencer():
    prod_vencimiento = []
    try:
        confi = ConfiEmpresa.objects.get(id=1)
        dias_compare = confi.dias_a_vencer
    except Exception as e:
        dias_compare = 30
        
    try:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")

        for p in productos:
            if p.fecha_vencimiento is not None:
                if rest_dates(p.fecha_vencimiento) <= dias_compare:
                    prod_vencimiento.append(p)

        total =  len(prod_vencimiento)
        return total
    except Exception as e:
        return 0

def total_vacunas_aplicadas():
    try:
        historico = HistoricoFichaMedica.objects.all()
        total =  historico.count()
        return total
    except Exception as e:
        return 0

def total_reservas_hoy():
    try:
        fecha_hoy = date(hoy.year, hoy.month, hoy.day)
        reservas = Reserva.objects.filter(fecha_reserva=fecha_hoy)
        total =  reservas.count()
        return total
    except Exception as e:
        return 0

def total_vacunas_proximas():
    ficha = []
    try:
        confi = ConfiEmpresa.objects.get(id=1)
        dias_compare = confi.dias_alert_vacunas
    except Exception as e:
        dias_compare = 30
    
    try:
        list_historico = HistoricoFichaMedica.objects.all()
        for f in list_historico:
            if f.fecha_proxima_aplicacion is not None:
                if rest_dates(f.fecha_proxima_aplicacion) <= dias_compare:
                    ficha.append(f)

        total =  len(ficha)
        return total
    except Exception as e:
        return 0

def cargar_vacunas_aplicadas():
    vacunas_aplicadas = HistoricoFichaMedica.objects.all()
    try:
        for va in vacunas_aplicadas:
            if va.historico_cargado_reporte == 'N':
                va.historico_cargado_reporte = 'S'
                va.save()
                try:
                    produc = VacunasAplicadas.objects.get(id_producto=va.vacuna.id_producto.id,
                                                          date=hoy)
                    if produc is not None:
                        produc.cantidad_aplicadas += 1
                        produc.save()
                    else:
                        produc = VacunasAplicadas()
                        pro_id = Producto.objects.get(id=va.vacuna.id_producto.id)
                        produc.id_producto = pro_id
                        produc.date = hoy
                        produc.cantidad_aplicadas = 1
                        produc.save()
                except Exception:
                    produc = VacunasAplicadas()
                    pro_id = Producto.objects.get(id=va.vacuna.id_producto.id)
                    produc.id_producto = pro_id
                    produc.date = hoy
                    produc.cantidad_aplicadas = 1
                    produc.save()
    except Exception as e:
        pass


def rest_dates(fecha_vencimiento):
    try:
        fecha_vencimiento_split = fecha_vencimiento.split('/')          
        fecha_vencimiento_compare = date(int(fecha_vencimiento_split[2]), int(fecha_vencimiento_split[1]), int(fecha_vencimiento_split[0]))
        return (fecha_vencimiento_compare - hoy).days if (fecha_vencimiento_compare - hoy).days >= 0 else 0
    except Exception as e:
        return 0
    
def get_reserva_today(request):
    data = []
    try:
        fecha_hoy = date(hoy.year, hoy.month, hoy.day)
        reservas = Reserva.objects.exclude(estado_re='FIN').filter(fecha_reserva=fecha_hoy)
        reservas = reservas.exclude(estado_re='CAN').all()
        
        total =  reservas.count()

        _start = request.GET.get('start')
        _length = request.GET.get('length')
        if _start and _length:
            start = int(_start)
            length = int(_length)           

            reservas = reservas[start:start + length]

        data =[{'cliente': r.id_cliente.nombre_cliente + '\n' + r.id_cliente.apellido_cliente,
                'mascota': r.id_mascota.nombre_mascota,'evento': 'Servicio: ' + r.id_servicio.nombre_servicio + '\n' + 'Horario: ' + r.hora_reserva} for r in reservas]        
            
        response = {
            'data': data,
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)
    except Exception as e:
        response = {
            'data': data,
            'recordsTotal': 0,
            'recordsFiltered': 0,
        }
        return JsonResponse(response)

def get_vacunas_today(request):
    data = []
    try:
        fecha_hoy = hoy.strftime("%d/%m/%Y")
        historico = HistoricoFichaMedica.objects.filter(fecha_proxima_aplicacion=fecha_hoy)
        
        total =  historico.count()

        _start = request.GET.get('start')
        _length = request.GET.get('length')
        if _start and _length:
            start = int(_start)
            length = int(_length)       

            historico = historico[start:start + length]

        data =[{'cliente': h.id_mascota.id_cliente.nombre_cliente + '\n' + h.id_mascota.id_cliente.apellido_cliente,
                'mascota': h.id_mascota.nombre_mascota, 'evento': 'Vacuna: ' + h.proxima_vacunacion} for h in historico]        
            
        response = {
            'data': data,
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)
    except Exception as e:
        response = {
            'data': data,
            'recordsTotal': 0,
            'recordsFiltered': 0,
        }
        return JsonResponse(response)
    

def cargar_servicios_vendidos():
    facturaVenta = CabeceraVenta.objects.exclude(is_active='N')
    try:
        if facturaVenta is not None:
            for fv in facturaVenta:
                facturaDetalle = DetalleVenta.objects.filter(id_factura_venta=fv.id)
                for factDet in facturaDetalle:
                    if factDet.tipo != 'P':
                        if factDet.detalle_cargado_servicio == 'N':
                            factDet.detalle_cargado_servicio = "S"
                            factDet.save()
                            try:
                                produc = ServicioVendido.objects.get(id_producto=factDet.id_producto.id,
                                                                     date=hoy)
                                if produc is not None:
                                    produc.cantidad_vendida_total += factDet.cantidad
                                    produc.save()
                                else:
                                    produc = ServicioVendido()
                                    pro_id = Producto.objects.get(id=factDet.id_producto.id)
                                    produc.id_producto = pro_id
                                    produc.date = hoy
                                    produc.cantidad_vendida_total = factDet.cantidad
                                    produc.save() 
                            except Exception as e:
                                produc = ServicioVendido()
                                pro_id = Producto.objects.get(id=factDet.id_producto.id)
                                produc.id_producto = pro_id
                                produc.date = hoy
                                produc.cantidad_vendida_total = factDet.cantidad
                                produc.save()
    except Exception as e:
        pass


def cargar_productos_vendidos():
    facturaVenta = CabeceraVenta.objects.exclude(factura_anulada='S')
    try:
        if facturaVenta is not None:
            for fv in facturaVenta:
                facturaDetalle = DetalleVenta.objects.filter(id_factura_venta=fv.id)
                for factDet in facturaDetalle:
                    if factDet.tipo != 'S':
                        if factDet.detalle_cargado_reporte == 'N':
                            factDet.detalle_cargado_reporte = "S"
                            factDet.save()
                            try:
                                produc = ProductoVendido.objects.get(id_producto=factDet.id_producto.id)
                                produc.cantidad_vendida_total += factDet.cantidad
                                produc.save()
                            except Exception as e:
                                produc = ProductoVendido()
                                pro_id = Producto.objects.get(id=factDet.id_producto.id)
                                produc.id_producto = pro_id
                                produc.cantidad_vendida_total = factDet.cantidad
                                produc.save()
    except Exception as e:
        pass

def cargar_producto_vendido_mes():
    facturaVenta = CabeceraVenta.objects.exclude(is_active='N')
    try:
        if facturaVenta is not None:
            for fv in facturaVenta:
                facturaDetalle = DetalleVenta.objects.filter(id_factura_venta=fv.id)
                for factDet in facturaDetalle:
                    if factDet.tipo != 'S':
                        if factDet.detalle_cargado_mes == 'N':
                            factDet.detalle_cargado_mes = "S"
                            factDet.save()
                            try:
                                produc = ProductoVendidoMes.objects.get(id_producto=factDet.id_producto.id,
                                                                           date=hoy)
                                if produc is not None:
                                    produc.cantidad_vendida_total += factDet.cantidad
                                    produc.save()
                                else:
                                    produc = ProductoVendidoMes()
                                    pro_id = Producto.objects.get(id=factDet.id_producto.id)
                                    produc.id_producto = pro_id
                                    produc.date = hoy
                                    produc.cantidad_vendida_total = factDet.cantidad
                                    produc.save()
                            except Exception as e:
                                produc = ProductoVendidoMes()
                                pro_id = Producto.objects.get(id=factDet.id_producto.id)
                                produc.id_producto = pro_id
                                produc.date = hoy
                                produc.cantidad_vendida_total = factDet.cantidad
                                produc.save()
    except Exception as e:
        pass

def convert_dates(desde, hasta):
    fecha_desde = "{}-{}-{}".format(desde.split('/')[2], desde.split('/')[1],
                                    desde.split('/')[0])
    fecha_hasta = "{}-{}-{}".format(hasta.split('/')[2], hasta.split('/')[1],
                                    hasta.split('/')[0])
    return "{}?{}".format(fecha_desde, fecha_hasta)