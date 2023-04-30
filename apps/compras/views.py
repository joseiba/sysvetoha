import json
import math
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from apps.compras.forms import ProveedorForm
from apps.compras.models import Proveedor
# Create your views here.


date = datetime.now()
today = date.strftime("%d/%m/%Y")
# Create your views here.
@login_required()
@permission_required('compras.add_proveedor')
def add_proveedor(request):
    form = ProveedorForm    
    if request.method == 'POST':
        form = ProveedorForm(request.POST) 
        if form.is_valid():           
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            # ruc = Ruc()
            # ruc.nro_ruc = request.POST.get('ruc_proveedor')
            # ruc.save()
            return redirect('/compra/listProveedor')
    context = {'form' : form}
    return render(request, 'compras/proveedor/add_proveedor_modal.html', context)

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
            # ruc = Ruc()
            # ruc.nro_ruc = request.POST.get('ruc_proveedor')
            # ruc.save()
            return redirect('/compra/listProveedor')
    context = {'form' : form, 'proveedor': proveedor}
    return render(request, 'compras/proveedor/edit_proveedor_modal.html', context)

@login_required()
@permission_required('compras.view_proveedor')
def list_proveedor(request):
    return render(request, "compras/proveedor/list_proveedor.html")

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
        page = math.ceil(start / length) + 1
        per_page = length

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
@login_required()
@permission_required('compras.delete_proveedor')
def delete_proveedor(request, id):
    proveedor = Proveedor.objects.get(id=id)
    if request.method == 'POST':
        proveedor.is_active = "N"
        proveedor.save()
        return redirect('/compra/listProveedor')
    context = {'proveedor': proveedor}
    return render(request, "compras/proveedor/baja_proveedor_modal.html", context)