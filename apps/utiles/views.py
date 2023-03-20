import json
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, date

from apps.utiles.models import Timbrado

from apps.ventas.models import CabeceraVenta, DetalleVenta

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
        list_validaciones = Ruc.objects.filter(nro_ruc=obj_validar)
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