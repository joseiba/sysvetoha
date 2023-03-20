from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import math


from apps.configuracion.configuracion_inicial.models import ConfiEmpresa
from apps.configuracion.configuracion_inicial.forms import ConfiEmpresaForm
from apps.inventario.depositos.models import Deposito
from apps.utiles.models import Timbrado

# Create your views here.
#Configuraciones iniciales
@login_required()
@permission_required('configuracion.add_confiempresa')
def confi_inicial(request):
    try:
        confi = ConfiEmpresa.objects.get(id=1) 
        confiUbi = ConfiEmpresa.objects.get(id=1)    
        form = ConfiEmpresaForm(instance=confi)
        if request.method == 'POST':
            form = ConfiEmpresaForm(request.POST, instance=confi)
            if not form.has_changed():
                messages.info(request, "No has hecho ningun cambio!")
                return redirect('/configuracion/confiInicial/')
            if form.is_valid():
                confi = form.save(commit=False)
                timbrado = Timbrado()
                timbrado_existe = Timbrado.objects.filter(nro_timbrado= request.POST.get('nro_timbrado'))
                if timbrado_existe.count() == 0:
                    timbrado.nro_timbrado = request.POST.get('nro_timbrado')
                    timbrado.fecha_inicio_timbrado = request.POST.get('fecha_inicio_timbrado')
                    timbrado.fecha_fin_timbrado = request.POST.get('fecha_fin_timbrado')
                    timbrado.save()
                confi.save() 
                try:
                    depo = Deposito.objects.get(descripcion=confiUbi.ubicacion_deposito_inicial)   
                    depo.descripcion =  request.POST.get('ubicacion_deposito_inicial')     
                    depo.save()
                except:                                              
                    depo = Deposito()
                    depo.descripcion = request.POST.get('ubicacion_deposito_inicial')
                    depo.save()

                messages.success(request, 'Se ha agregado correctamente!')
                return redirect('/configuracion/confiInicial/')
    except Exception as e:
        pass
    context = {'form' : form}
    return render(request, 'configuracion/configuracion_inicial/confi_inicial.html', context)   

@login_required()
@permission_required('configuracion.view_confiempresa')
def list_historial_timbrado(request):
    return render(request,"configuracion/configuracion_inicial/list_historial_timbrado.html")

@login_required()
def get_historial_timbrado_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        timbra = Timbrado.objects.filter(Q(nro_timbrado__icontains=query))
        timbra = timbra.order_by('id')
    else:
        timbra = Timbrado.objects.all().order_by('id')
        timbra = timbra.order_by('id')

    total = timbra.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        timbra = timbra[start:start + length]

    data = [{'id': t.id, 'nro_timbrado': t.nro_timbrado, 'fecha_inicio': t.fecha_inicio_timbrado,
            'fecha_fin': t.fecha_fin_timbrado, 'estado': t.vencido} for t in timbra]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)