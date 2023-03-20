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

from apps.inventario.depositos.forms import DepositoForm
from apps.inventario.depositos.models import Deposito

date = datetime.now()

# Create your views here.

#Metodo para agregar deposito
@login_required()
@permission_required('depositos.view_deposito')
def add_deposito(request):
    form = DepositoForm
    if request.method == 'POST':
        form = DepositoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Deposito agregado correctamente!')
            return redirect('/deposito/list')   
    context = {'form' : form}
    return render(request, 'inventario/depositos/add_deposito.html', context)

# Metodo para editar deposito
@login_required()
@permission_required('depositos.change_deposito')
def edit_deposito(request, id):
    deposito = Deposito.objects.get(id=id)
    form = DepositoForm(instance=deposito)
    if request.method == 'POST':
        form = DepositoForm(request.POST, instance=deposito)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/deposito/list/')
        if form.is_valid():
            deposito = form.save(commit=False)
            deposito.save()
            messages.add_message(request, messages.SUCCESS, 'El depósito se ha editado correctamente!')
            return redirect('/deposito/list/')

    context = {'form': form, 'deposito': deposito}
    return render(request, 'inventario/depositos/add_deposito.html', context)

#Metodo para listar todos los depositos
@login_required()
@permission_required('depositos.view_deposito')
def list_deposito(request):
    return render(request, "inventario/depositos/list_deposito.html")


def get_list_deposito(request):
    query = request.GET.get('busqueda')
    if query:
        depositos = Deposito.objects.filter(Q(descripcion__icontains=query)).order_by('-last_modified')
    else:
        depositos = Deposito.objects.all().order_by('-last_modified')

    total = depositos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        depositos = depositos[start:start + length]

    data = [{'id': de.id, 'descripcion': de.descripcion } for de in depositos]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response) 
