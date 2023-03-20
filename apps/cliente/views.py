from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import math

from apps.cliente.forms import CiudadForm, ClienteForm
from apps.cliente.models import Ciudad, Cliente

#Ciudades 
#@login_required()
#@permission_required('configuracion.add_confiempresa')
def add_ciudad(request):
    form = CiudadForm
    if request.method == 'POST':
        form = CiudadForm(request.POST or None)
        if form.is_valid():
            messages.success(request, 'Se ha agregado correctamente!')
            form.save()
            return redirect('/configuracion/listCiudades/')
    context = {'form' : form}
    return render(request, 'configuracion/ciudad/add_ciudad_modal.html', context)


#@login_required()
#@permission_required('configuracion.change_confiempresa')
def edit_ciudad(request, id):
    ciudad = Ciudad.objects.get(id=id)
    form = CiudadForm(instance=ciudad)
    if request.method == 'POST':
        form = CiudadForm(request.POST, instance=ciudad)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/configuracion/listCiudades/')
        if form.is_valid():
            ciudad = form.save(commit=False)
            ciudad.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/configuracion/listCiudades/')
    context = {'form' : form, 'ciudad': ciudad}
    return render(request, 'configuracion/ciudad/edit_ciudad_modal.html', context)

#@login_required()
#@permission_required('configuracion.view_confiempresa')
def list_ciudades(request):
    return render(request, 'configuracion/ciudad/list_ciudad.html')

#@login_required()
def get_list_ciudades(request):
    query = request.GET.get('busqueda')
    if query != "":
        ciudad = Ciudad.objects.filter(Q(nombre_ciudad__icontains=query))
    else:
        ciudad = Ciudad.objects.all()

    total = ciudad.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        ciudad = ciudad[start:start + length]

    data = [{'id': c.id, 'nombre': c.nombre_ciudad} for c in ciudad]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

#Area de clientes
#@login_required()
#@permission_required('cliente.add_cliente')
def add_cliente(request):
    form = ClienteForm
    if request.method == 'POST':
        form = ClienteForm(request.POST or None)
        if form.is_valid():           
            messages.success(request, 'Se ha agregado correctamente!')
            form.save()
            return redirect('/cliente/listCliente')
    ciudades = Ciudad.objects.all()
    context = {'form' : form, 'ciudades' : ciudades}
    return render(request, 'cliente/add_modal_cliente.html', context)

# Metodo para editar Clientes
#@login_required()
#@permission_required('cliente.change_cliente')
def edit_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    form = ClienteForm(instance=cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/cliente/listCliente/')
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()          
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/cliente/listCliente/')
    
    ciudades = Ciudad.objects.all()
    context = {'form': form, 'cliente':cliente, 'ciudades': ciudades}
    return render(request, 'cliente/add_modal_cliente.html', context)

#Metodo para eliminar cliente
#@login_required()
#@permission_required('cliente.delete_cliente')
def inactivar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    if request.method == 'POST':
        print("post")
        cliente.is_active = "N"
        cliente.save()
        return redirect('/cliente/listCliente/')
    context = {'cliente': cliente}
    print("pantalla")
    return render(request, 'cliente/baja_cliente.html', context)
    

#Metodo para listar todos los clientes
# @login_required()
# @permission_required('cliente.view_cliente')
def list_clientes(request):    
    return render(request, "cliente/list_cliente.html")

# @login_required()
def list_client_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        clientes = Cliente.objects.exclude(is_active="N").filter(Q(nombre_cliente__icontains=query) 
        | Q(cedula__icontains=query) | Q(apellido_cliente__icontains=query)
        | Q(id_ciudad__nombre_ciudad__icontains=query)).order_by('last_modified')
    else:
        clientes = Cliente.objects.exclude(is_active="N").order_by('-last_modified')

    total = clientes.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        clientes = clientes[start:start + length]

    data = [{'id': clie.id, 'nombre': clie.nombre_cliente, 'apellido': clie.apellido_cliente, 
        'cedula': clie.cedula, 'telefono': clie.telefono, 'direccion': clie.direccion, 'ciudad': clie.id_ciudad.nombre_ciudad } 
        for clie in clientes]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)