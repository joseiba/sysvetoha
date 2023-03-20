from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import math

from apps.configuracion.empleado.forms import EmpleadoForm
from apps.configuracion.empleado.models import Empleado

# Create your views here.
#Empleados 
@login_required()
@permission_required('empleado.add_empleado')
def add_empleado(request):
    form = EmpleadoForm    
    if request.method == 'POST':
        form = EmpleadoForm(request.POST) 
        if form.is_valid():           
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')          
            return redirect('/configuracion/listEmpleado/')
    context = {'form' : form}
    return render(request, 'configuracion/empleado/add_empleado_modal.html', context)

@login_required()
@permission_required('empleado.change_empleado')
def edit_empleado(request, id):
    emp = Empleado.objects.get(id=id)
    form = EmpleadoForm(instance=emp)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=emp)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/configuracion/listEmpleado/')
        if form.is_valid():
            emp = form.save(commit=False)
            emp.save()            
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/configuracion/listEmpleado/')
    context = {'form' : form, 'emp': emp}
    return render(request, 'configuracion/empleado/edit_empleado_modal.html', context)


@login_required()
@permission_required('empleado.view_empleado')
def list_empleado(request):
    emp = Empleado.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(emp, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "configuracion/empleado/list_empleados.html", context)

@login_required()
def get_list_empleados_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        emp = Empleado.objects.exclude(is_active="N").filter(Q(nombre_emp__icontains=query) | Q(apellido_emp__icontains=query)
            | Q(ci_empe__icontains=query) | Q(id_servicio__nombre_servicio__icontains=query))
    else:
        emp = Empleado.objects.exclude(is_active="N").order_by('-last_modified')

    total = emp.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        emp = emp[start:start + length]

    data = [{'id': e.id, 'nombre': e.nombre_emp, 'apellido': e.apellido_emp, 'cedula': e.ci_empe, 'disponible': e.disponible,
        'nombre_servicio': e.id_servicio.nombre_servicio} for e in emp]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@permission_required('empleado.delete_empleado')
def bajar_empleado(request, id):
    emp = Empleado.objects.get(id=id)
    if request.method == 'POST':
        emp.is_active = "N"
        emp.save()
        messages.success(request, 'Se ha dado de baja correctamente!')
        return redirect('/configuracion/listEmpleado/')
    context = {'emp': emp}
    return render(request, "configuracion/empleado/baja_empleado_modal.html", context)

@login_required()
def search_empleado(request):
    query = request.GET.get('q')
    if query:
        emp = Empleado.objects.exclude(is_active="N").filter(Q(nombre_emp__icontains=query))
    else:
        emp = Empleado.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(emp, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "configuracion/empleado/list_empleados.html", context)