from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import math

from apps.configuracion.tipo_vacuna.forms import TipoVacunaForm
from apps.configuracion.tipo_vacuna.models import TipoVacuna

# Create your views here.
@login_required()
@permission_required('configuracion.add_tipovacuna')
def add_vacuna(request):
    form = TipoVacunaForm
    if request.method == 'POST':
        form = TipoVacunaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/configuracion/listVacunas')
    context = {'form' : form}
    return render(request, 'configuracion/vacunas/add_tipo_vacunas.html', context)

@login_required()
@permission_required('configuracion.change_tipovacuna')
def edit_vacuna(request, id):
    vacu = TipoVacuna.objects.get(id=id)
    form = TipoVacunaForm(instance=vacu)
    if request.method == 'POST':
        form = TipoVacunaForm(request.POST, instance=vacu)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/configuracion/listVacunas')
        if form.is_valid():
            vacu = form.save(commit=False)
            vacu.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/configuracion/listVacunas/')
    context = {'form' : form, 'vacu': vacu}
    return render(request, 'configuracion/vacunas/edit_tipo_vacunas.html', context)    

@login_required()
@permission_required('configuracion.view_tipovacuna')
def list_vacunas(request):
    return render(request, "configuracion/vacunas/list_tipos_vacunas.html")

@login_required()
def get_list_vacunas_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        vacu = TipoVacuna.objects.filter(Q(nombre_vacuna__icontains=query))
    else:
        vacu = TipoVacuna.objects.all()

    total = vacu.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        vacu = vacu[start:start + length]

    data = [{'id': va.id, 'nombre_vacuna': va.nombre_vacuna, 'periodo': va.periodo_aplicacion } for va in vacu]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response) 


def get_periodo_vacunacion(request):
    mensaje = ""
    try:
        vacuna = TipoVacuna.objects.get(id=request.GET.get("tipo"))
        response = {'mensaje': mensaje, 'periodo': vacuna.periodo_aplicacion}
        return JsonResponse(response) 
    except Exception as e:
        mensaje = "error"
        response = {'mensaje': mensaje}
        return JsonResponse(response) 
